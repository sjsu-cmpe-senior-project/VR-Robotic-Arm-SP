# LeapCxx
Implementation of LeapAPI (1.0-3.0) using LeapC

### Requirements
  * [LeapSDK 4.0.0](https://developer.leapmotion.com/releases/leap-motion-orion-400)
    * Install Leap_Motion_Service_Setup
  * [CMake 3.10+](https://cmake.org/download/)
    * It is a cross-platform free and open source software tool for managing the build process of software using a compiler-independent method
  * [LeapCxx](https://github.com/leapmotion/LeapCxx)
    * Already included in this directory
  * C++11 compliant compiler


### Building LeapCxx
LeapCxx builds using CMake 3.10 or higher. See the [CMake documentation](https://cmake.org/cmake/help/latest/)
for more information on using CMake, and the LeapSDK Readme for information specific to using the SDK with 
CMake.

### Quick Start with CMake GUI -- Windows
On GUI for:
  * `Source Code` set to `pwd/LeapCxx_4.0`
  * `Build Binaries` set to `pwd/LeapCxx_4.0/build`
    * Note: Delete contents of binaries, if it is the first time compiling the code on your machine
  * Click `Configure`, select Generator to `Microsoft Visual Studio`    or other IDE with a gcc debugger. 
  * CMake must know where to find the LeapSDK, so either set `CMAKE_PREFIX_PATH` to the directory contraining the LeapSDK, or set `LeapSDK_DIR` to `your_path\LeapDSK_4.0.0\LeapSDK\lib\cmake\LeapSDK`
    * `LeapSDK_DIR` reference variable will show up in CMake GUI after clicking `Configure` 
  * Uncheck the `BUILD_SWIG` and `BUILD_TESTING` boxes. Leave `BUILD_SAMPLES` box checked.
  * Click `Generate`
    * Note: disregard the CMake Warning (dev)...
  * Lastly, click `Open Project`
  * Once inside your IDE, select the SampleCxx as the target and run the debugger. **Make sure your Leap Motion Controller is connected to your PC before running the debugger**


### Building Samples
All the samples have build steps defined as part of the cmake projects.
