To do list
==========

* Write program tests.  At least for the batch program.
* Write a program test that certifies the program is safe to run even when the final
   formulated path points to the original file or directory.  This protects against data
   loss from organizing an already-organized path.
* Implement litmus unit test that uses my archive data to see if would archive files the way I would.
* Implement configurable subdir hints for the different natures.  The hints system kind of sucks.
  Ideally, I would like the nature to tell me what bits of information are available in a key value
  format perhaps, and the destination to look for the proper values within several levels deep of the
  destination (so that structures like TV/Drama/Private Practice/ and Music/A/Ace of Base can be
  automatically supported).  Of course, the user should be able to override both how the structure
  is formed (using some templating language) and also specific strings that fail to match anything
  in the destination structure.
* Implement GUI that can be launched from Nautilus or Dolphin (text file already exists)
  UI must be in GTK+ because a Qt UI would be unbearably slow over the network.