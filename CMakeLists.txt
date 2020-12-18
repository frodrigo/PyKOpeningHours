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

# FetchContent would make all this simpler, but it requires cmake >= 3.11
if (EXISTS "/etc/debian_version") # GNUInstallDirs only does this if the prefix is /usr, ECM does it always
    set(CMAKE_INSTALL_LIBDIR "lib/${CMAKE_LIBRARY_ARCHITECTURE}")
endif()
set(kopeninghours_lib "${EXTERNAL_PROJECTS_PREFIX}/${CMAKE_INSTALL_LIBDIR}/${CMAKE_STATIC_LIBRARY_PREFIX}KOpeningHours${CMAKE_STATIC_LIBRARY_SUFFIX}")

ExternalProject_Add(KOpeningHoursExternal
    PREFIX "${EXTERNAL_PROJECTS_PREFIX}"
    GIT_REPOSITORY https://invent.kde.org/libraries/kopeninghours.git
    GIT_TAG "3cd8d78"
    CMAKE_ARGS
       -DVALIDATOR_ONLY=TRUE
       -DBUILD_SHARED_LIBS=FALSE
       -DCMAKE_INSTALL_PREFIX=${EXTERNAL_PROJECTS_PREFIX}
       -DCMAKE_BUILD_TYPE=Release
    LOG_BUILD 0 # show errors on stderr
    BUILD_BYPRODUCTS <INSTALL_DIR>/${CMAKE_INSTALL_LIBDIR}/${CMAKE_STATIC_LIBRARY_PREFIX}KOpeningHours${CMAKE_STATIC_LIBRARY_SUFFIX}
)
add_dependencies(KOpeningHoursExternal ECMExternal)
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

set(SRC PyKOpeningHours)

add_library(PyKOpeningHours MODULE
    ${SRC}/pykopeninghours.cpp
    ${SRC}/python_qt_wrappers.cpp
    test.py # just so it appears in QtCreator
)

target_compile_definitions(PyKOpeningHours PRIVATE KOPENINGHOURS_VALIDATOR_ONLY)

# Set up the libraries and header search paths for this target
target_link_libraries(PyKOpeningHours PUBLIC ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} KOpeningHours)
target_include_directories(PyKOpeningHours PRIVATE ${PYTHON_INCLUDE_DIRS})

set(_install_dir lib/python${PYTHONLIBS_VERSION_MAJOR}.${PYTHONLIBS_VERSION_MINOR}/site-packages)

install(TARGETS PyKOpeningHours DESTINATION ${_install_dir}/PyKOpeningHours)
install(FILES ${SRC}/PyKOpeningHours.pyi ${SRC}/__init__.py DESTINATION ${_install_dir}/PyKOpeningHours)
