cmake_minimum_required(VERSION 3.5)

project(PyKOpeningHours VERSION 1.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find python and Boost - both are required dependencies
find_package(PythonLibs 3.6 REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)
find_package(Qt5 COMPONENTS Core REQUIRED)

# Build KOpeningHours automatically
include(GNUInstallDirs) # sets CMAKE_INSTALL_LIBDIR
include(ExternalProject)
set(KOPENINGHOURS_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/external")
ExternalProject_Add(KOpeningHoursExternal
   PREFIX "${KOPENINGHOURS_PREFIX}"
   GIT_REPOSITORY https://invent.kde.org/libraries/kopeninghours.git
   GIT_TAG "6c903a0"
   CMAKE_ARGS
       -DPARSER_ONLY=TRUE
       -DCMAKE_INSTALL_PREFIX=${KOPENINGHOURS_PREFIX}
       -DCMAKE_BUILD_TYPE=Release
   LOG_BUILD 0 # show errors on stderr
)
# FetchContent would make all this simpler, but it requires cmake >= 3.11
set(kopeninghours_lib "${KOPENINGHOURS_PREFIX}/${CMAKE_INSTALL_LIBDIR}/${CMAKE_SHARED_LIBRARY_PREFIX}KOpeningHours${CMAKE_SHARED_LIBRARY_SUFFIX}")
add_library(KOpeningHours IMPORTED SHARED)
set_target_properties(KOpeningHours PROPERTIES
   IMPORTED_LOCATION "${kopeninghours_lib}"
   INTERFACE_LINK_LIBRARIES Qt5::Core
)
add_dependencies(KOpeningHours KOpeningHoursExternal)
# workaround for https://gitlab.kitware.com/cmake/cmake/-/issues/15052
include_directories("${KOPENINGHOURS_PREFIX}/include")

#find_package(KOpeningHours REQUIRED)

# Without this, any build libraries automatically have names "lib{x}.so"
set(CMAKE_SHARED_MODULE_PREFIX "")

add_library(PyKOpeningHours MODULE
    pykopeninghours.cpp
    python_qt_wrappers.cpp
    test.py # just so it appears in QtCreator
)

# Set up the libraries and header search paths for this target
target_link_libraries(PyKOpeningHours PUBLIC ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} KOpeningHours)
target_include_directories(PyKOpeningHours PRIVATE ${PYTHON_INCLUDE_DIRS})
