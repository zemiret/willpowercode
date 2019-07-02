# willpowercode

A project that allows you to write code using your willpower!

This project strives to provide something that will look as if
you're writing code using your willpower through the use of:

* OpenCV for gesture detection (namely the number of fingers shown)
* running vim scripts for text generation

## Setup:
It's recommended to use *virtualenv*.

Run:
```
pip install -r requirements
```

Keep in mind that detection algorithms require very stable
camera and lightning conditions for now.

## Run
This project is WIP. You can run `python src/main.py`
but it's in "testing stage" for now.

## Bonus
Checkout branch `snake`.
You can play snake using the number of fingers shown to the camera.
When you clench your fist you accept the input you've been showing to the camera
since the last time you accepted.

