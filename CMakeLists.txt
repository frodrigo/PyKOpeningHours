cmake_minimum_required(VERSION 3.5)

project(PyKOpeningHours VERSION 1.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(PythonLibs 3.6 REQUIRED)
# Extract major/minor python version
string(REPLACE "." ";" VERSION_LIST ${PYTHONLIBS_VERSION_STRING})
list(GET VERSION_LIST 0 PYTHONLIBS_VERSION_MAJOR)
list(GET VERSION_LIST 1 PYTHONLIBS_VERSION_MINOR)

# boost-python requires exact version number
find_package(Boost COMPONENTS python${PYTHONLIBS_VERSION_MAJOR}${PYTHONLIBS_VERSION_MINOR} REQUIRED)
find_package(Qt5 COMPONENTS Core REQUIRED)

# Build KOpeningHours automatically, starting with ECM
include(GNUInstallDirs) # sets CMAKE_INSTALL_LIBDIR
include(ExternalProject)
set(EXTERNAL_PROJECTS_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/external")

ExternalProject_Add(ECMExternal
   PREFIX "${EXTERNAL_PROJECTS_PREFIX}"
   GIT_REPOSITORY https://invent.kde.org/frameworks/extra-cmake-modules.git
   GIT_TAG "v5.77.0"
   CMAKE_ARGS
       -DBUILD_TESTING=FALSE
       -DCMAKE_DISABLE_FIND_PACKAGE_Sphinx=TRUE
       -DCMAKE_INSTALL_PREFIX=${EXTERNAL_PROJECTS_PREFIX}
   LOG_BUILD 0 # show errors on stderr
)

ExternalProject_Add(KOpeningHoursExternal
    PREFIX "${EXTERNAL_PROJECTS_PREFIX}"
    GIT_REPOSITORY https://invent.kde.org/libraries/kopeninghours.git
    GIT_TAG "73a2ff2"
    CMAKE_ARGS
       -DVALIDATOR_ONLY=TRUE
       -DCMAKE_INSTALL_PREFIX=${EXTERNAL_PROJECTS_PREFIX}
       -DCMAKE_BUILD_TYPE=Release
    LOG_BUILD 0 # show errors on stderr
)
add_dependencies(KOpeningHoursExternal ECMExternal)
# FetchContent would make all this simpler, but it requires cmake >= 3.11
if (EXISTS "/etc/debian_version") # GNUInstallDirs only does this if the prefix is /usr, ECM does it always
    set(CMAKE_INSTALL_LIBDIR "lib/${CMAKE_LIBRARY_ARCHITECTURE}")
endif()
set(kopeninghours_lib "${EXTERNAL_PROJECTS_PREFIX}/${CMAKE_INSTALL_LIBDIR}/${CMAKE_SHARED_LIBRARY_PREFIX}KOpeningHours${CMAKE_SHARED_LIBRARY_SUFFIX}")
add_library(KOpeningHours IMPORTED SHARED)
set_target_properties(KOpeningHours PROPERTIES
    IMPORTED_LOCATION "${kopeninghours_lib}"
    INTERFACE_LINK_LIBRARIES Qt5::Core
)
add_dependencies(KOpeningHours KOpeningHoursExternal)
# workaround for https://gitlab.kitware.com/cmake/cmake/-/issues/15052
include_directories("${EXTERNAL_PROJECTS_PREFIX}/include")

#find_package(KOpeningHours REQUIRED)

# Without this, any build libraries automatically have names "lib{x}.so"
set(CMAKE_SHARED_MODULE_PREFIX "")

add_library(PyKOpeningHours MODULE
    pykopeninghours.cpp
    python_qt_wrappers.cpp
    test.py # just so it appears in QtCreator
)

target_compile_definitions(PyKOpeningHours PRIVATE KOPENINGHOURS_VALIDATOR_ONLY)

# Set up the libraries and header search paths for this target
target_link_libraries(PyKOpeningHours PUBLIC ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} KOpeningHours)
target_include_directories(PyKOpeningHours PRIVATE ${PYTHON_INCLUDE_DIRS})
