# this example demonstrates full loading/unloading
# of transport layers to allow full shutdown of the
# hardware associated with the transport layer

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# this sequence of calls should only be used
# if you need _full control_ over the object lifetimes
# e.g. if you need to powerdown a framegrabber in an
#      embedded setup.
# the standard API to create a device is via TlFactory
# as demonstrated in the grab.py sample
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import pypylon.pylon as py


tlf = py.TlFactory.GetInstance()


# load the transport layer
tl = tlf.CreateTl("BaslerGTC/Basler/CXP")

cam = py.InstantCamera()

# instantiate the first device on the transport
# layer
dev = tl.CreateFirstDevice()
# attach the device to the InstantCamera class
cam.Attach(dev)

cam.Open()
# ... work with the camera
cam.Close()


# detach the the device from the InstantCamera
# and release the device with the returned
# device handle
tl.DestroyDevice(cam.DetachDevice())

# unload the transport layer
tlf.ReleaseTl(tl)

# delete the now empty python objects
# to prevent further access from python side
del cam
del dev
del tl

# now all references to the transport layer
# hardware are released.
