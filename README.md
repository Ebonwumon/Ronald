##RONALD THE GPS##
He does python pathfinding and doesn't afraid of anything

Project is a collaboration is between Troy Pavlek and Victoria Bobey.

Some notes on running the project: It should all be generally handled by server.py. If server.py is running as main then it instantiates objects of itself and directs people around edmonton like nobody's business. If you want to run doctests on it, simply comment the main loop and use the doctest function at the bottom or you can run the testmod module externally on the server module.


There are some doctests that don't run (they're not preceeded by >>>) All of these tests "work"(tm) - they're usually just very slow or in the case of parse_input I couldn't figure out how to propery catch the exceptions thrown in the doctest and didn't recieve a reply on the forum - it should simply return a (in the end) typerror. Python was getting all up in my pancakes throwing its own exceptions.

I'm aware that if you enter improper inputs the program just explodes - the spec didn't define behaviour and I prefer this one because it teaches people the hard way not to mess with my programs (like Malcolm, I prefer to solve my problems with a chainsaw).
