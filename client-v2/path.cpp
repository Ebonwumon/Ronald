#include <Arduino.h>
#include <Adafruit_ST7735.h>
#include <SD.h>
#include <mem_syms.h>

#include "map.h"
#include "serial_handling.h"

// #define DEBUG_PATH

/* path routine error code
   0 no error
   1 
*/
int16_t path_errno;

extern Adafruit_ST7735 tft;

// read a path from the serial port and return the length of the
// path and a pointer to the array of coordinates.  That array should
// be freed later.

// Returns 1 if the call was successful, 0 if not.

uint8_t read_path(uint16_t *length_p, coord_t *path_p[]) {
    // the line to be read, and it size
    const uint8_t line_size = 40;
    char line[line_size];
    uint16_t bytes_read;

    // the field extracted
    const uint8_t field_size = 20;
    char field[field_size];
    uint16_t field_index;
    int32_t field_value;

    *length_p = 0;
    *path_p = 0;

    // reset the error code
    path_errno = 0;

    while ( ! Serial.available() )  { };

    uint16_t max_path_size = (AVAIL_MEM - 256) / sizeof(coord_t);

    #ifdef DEBUG_PATH
        Serial.print("Max path length ");
        Serial.println(max_path_size);
    #endif

    bytes_read = serial_readline(line, line_size);

    // read the number of points, first field
    field_index = 0;   
    field_index = 
        string_read_field(line, field_index, field, field_size, " ");
    field_value = string_get_int(field);

    #ifdef DEBUG_PATH
        Serial.print("Path length ");
        Serial.print(field_value);
        Serial.println();
    #endif

    // do a consistency check
    if ( field_value < 0  || max_path_size < field_value ) {
        path_errno = 1;
        return 0;
        }
    uint8_t tmp_length = field_value;
    *length_p = tmp_length;

    // allocate the storage, see if we got it.
    coord_t *tmp_path = (coord_t *) malloc( tmp_length * sizeof(coord_t));
    if ( !tmp_path ) { 
        path_errno = 2;
        return 0; 
        }

    *path_p = tmp_path;

    while ( tmp_length > 0 ) {
        bytes_read = serial_readline(line, line_size);

        // read the number of points, first field
        field_index = 0;   

        field_index = 
            string_read_field(line, field_index, field, field_size, " ");
        tmp_path->lat = string_get_int(field);

        field_index = 
            string_read_field(line, field_index, field, field_size, " ");
        tmp_path->lon = string_get_int(field);

        tmp_length--;
        tmp_path++;
        }

    return 1;
    }

uint8_t is_coord_visible(coord_t point) {
    // figure out the x and y positions on the current map of the 
    // given point
    uint16_t point_map_y = latitude_to_y(current_map_num, point.lat);
    uint16_t point_map_x = longitude_to_x(current_map_num, point.lon);

    uint8_t r = 
        screen_map_x < point_map_x &&
        point_map_x < screen_map_x + display_window_width &&
        screen_map_y < point_map_y &&
        point_map_y < screen_map_y + display_window_height; 

    return r;
}

void draw_path(uint16_t length, coord_t path[]) {
    // Print off the recieved path
    Serial.println("Path Received: ");
    for (uint8_t i=0; i<length; i++){
    #ifdef DEBUG_PATH 
        Serial.print(i);
        Serial.print(": ");
        Serial.print(path[i].lon);
        Serial.print(", ");
        Serial.println(path[i].lat);
    #endif
    }

    int32_t first_in_path_x = longitude_to_x(current_map_num, path[0].lon);
    int32_t first_in_path_y = latitude_to_y(current_map_num, path[0].lat);

    //Move screen so start of map is in the middle of the screen
    //move_window_to(first_in_path_x+60, first_in_path_y+60);
    //Draw a rectangle here for testing purposes
    //tft.drawRect( first_in_path_x, first_in_path_y, 14, 14, ST7735_BLUE);

    //Run through coords, draw visible lines
    for (uint8_t i=0; i<length; i++){
    #ifdef DEBUG_PATH
        Serial.print(i);
        Serial.print(" to ");
        Serial.print(i+1);
        Serial.print(": ");
    #endif

        //If both point are visible, draw the line between them
        if( is_coord_visible(path[i]) && is_coord_visible(path[i+1]) ){
            //Serial.println("Visible");
            int32_t start_x = longitude_to_x(current_map_num, path[i].lon) - screen_map_x;
            int32_t start_y = latitude_to_y(current_map_num, path[i].lat) - screen_map_y;
            int32_t stop_x = longitude_to_x(current_map_num, path[i+1].lon) - screen_map_x;
            int32_t stop_y = latitude_to_y(current_map_num, path[i+1].lat) - screen_map_y;
            //#ifdef DEBUG_PATH
            Serial.print("Start Converted to: ");
            Serial.print(start_x);
            Serial.print(", ");
            Serial.print(start_y);
            Serial.print(" Stop Converted to: ");
            Serial.print(stop_x);
            Serial.print(", ");
            Serial.println(stop_y);
            //#endif
            
            //tft.fillScreen(ST7735_BLACK);
            tft.drawLine(start_x, start_y, stop_x, stop_y, ST7735_BLUE);
        }
        else {
            //Serial.println("Not Visible");
        }
    }
}
