include(CheckCXXCompilerFlag)

# Find a compatible compiler flag from a series of list of possible flags
# For each list of whitespace separated compiler flags passed in argument, this
# function will append or save the compatible flags in ${var_prefix}_c and
# ${var_prefix}_cxx (if C++ is enabled)
macro(check_compiler_flags var_prefix)
  set(_cxx_opts)

  foreach(_flag_list ${ARGN})
    separate_arguments(_flag_list)

    foreach(_flag ${_flag_list})
      # Drop the first character (most likely either '-' or '/')
      string(SUBSTRING ${_flag}
                       1
                       -1
                       _flag_name)
      string(REGEX
             REPLACE "[-:/]"
                     "_"
                     _flag_name
                     ${_flag_name})

      check_cxx_compiler_flag(${_flag} cxx_compiler_has_${_flag_name})
      if(cxx_compiler_has_${_flag_name})
        list(APPEND _cxx_opts ${_flag})
        break()
      endif()
    endforeach()
  endforeach()

  if(DEFINED ${var_prefix}_cxx)
    list(APPEND ${var_prefix}_cxx ${_cxx_opts})
  else()
    set(${var_prefix}_cxx ${_cxx_opts})
  endif()
endmacro()

# ==============================================================================

macro(add_avx2_to_target target)
  if(NOT _avx2_flag_cxx)
    message(FATAL_ERROR "Compiler does not support AVX2 support. This is "
                        "required for target: ${target}")
  endif()
  target_compile_options(${target} PRIVATE ${_avx2_flag_cxx})
endmacro(add_avx2_to_target)

# ==============================================================================

macro(define_target
      namespace
      comp
      incpath)
  string(TOUPPER ${comp} uppercomponent)
  add_library(${namespace}::${comp} UNKNOWN IMPORTED)
  if(incpath)
    set_target_properties(${namespace}::${COMPONENT}
                          PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${incpath}")
  endif()
  if(EXISTS "${${namespace}_${uppercomponent}_LIBRARY}")
    set_target_properties(
      ${namespace}::${comp}
      PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES
                 "CXX"
                 IMPORTED_LOCATION
                 "${${namespace}_${uppercomponent}_LIBRARY}")
  endif()
  if(EXISTS "${${namespace}_${uppercomponent}_LIBRARY_RELEASE}")
    set_property(TARGET ${namespace}::${comp}
                 APPEND
                 PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
    set_target_properties(
      ${namespace}::${comp}
      PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE
                 "CXX"
                 IMPORTED_LOCATION_RELEASE
                 "${${namespace}_${uppercomponent}_LIBRARY_RELEASE}")
  endif()
  if(EXISTS "${${namespace}_${uppercomponent}_LIBRARY_DEBUG}")
    set_property(TARGET ${namespace}::${comp}
                 APPEND
                 PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
    set_target_properties(
      ${namespace}::${comp}
      PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG
                 "CXX"
                 IMPORTED_LOCATION_DEBUG
                 "${${namespace}_${uppercomponent}_LIBRARY_DEBUG}")
  endif()
  message(STATUS "${comp} | ${${namespace}_${uppercomponent}_DEPENDENCIES}")
  if(${namespace}_${uppercomponent}_DEPENDENCIES)
    unset(${namespace}_${uppercomponent}_TARGET_DEPENDENCIES)
    foreach(dep ${${namespace}_${uppercomponent}_DEPENDENCIES})
      list(APPEND ${namespace}_${uppercomponent}_TARGET_DEPENDENCIES
                  Boost::${dep})
    endforeach()
    if(COMPONENT STREQUAL "thread")
      list(APPEND ${namespace}_${uppercomponent}_TARGET_DEPENDENCIES
                  Threads::Threads)
    endif()
    set_target_properties(
      ${namespace}::${comp}
      PROPERTIES INTERFACE_LINK_LIBRARIES
                 "${${namespace}_${uppercomponent}_TARGET_DEPENDENCIES}")
  endif()
endmacro(define_target)

# ==============================================================================

# Properly set output directory for a target so that during an installation
# using either 'pip install' or 'python3 setup.py install' the build libraries
# get built in the proper directory
macro(setup_target_for_python_setup target)
  string(TOUPPER ${target} _TARGET)
  if(${_TARGET}_LIBRARY_OUTPUT_DIRECTORY)
    set_target_properties(${target}
                          PROPERTIES LIBRARY_OUTPUT_DIRECTORY
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_DEBUG
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_RELEASE
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY})
  endif(${_TARGET}_LIBRARY_OUTPUT_DIRECTORY)
endmacro(setup_target_for_python_setup)

# ==============================================================================

set(_boost_test_list)
macro(add_boost_test SOURCE_FILE_NAME)
  get_filename_component(TEST_EXECUTABLE_NAME ${SOURCE_FILE_NAME} NAME_WE)

  add_executable(${TEST_EXECUTABLE_NAME} ${SOURCE_FILE_NAME})
  target_link_libraries(${TEST_EXECUTABLE_NAME}
                        PRIVATE ${ARGN} Boost::unit_test_framework)

  list(APPEND _boost_test_list ${TEST_EXECUTABLE_NAME})

  file(READ "${SOURCE_FILE_NAME}" SOURCE_FILE_CONTENTS)
  string(REGEX MATCHALL
               "BOOST_AUTO_TEST_CASE\\( *([A-Za-z_0-9]+) *\\)"
               FOUND_TESTS
               ${SOURCE_FILE_CONTENTS})

  foreach(HIT ${FOUND_TESTS})
    string(REGEX
           REPLACE ".*\\( *([A-Za-z_0-9]+) *\\).*"
                   "\\1"
                   TEST_NAME
                   ${HIT})

    add_test(NAME "${TEST_EXECUTABLE_NAME}.${TEST_NAME}"
             COMMAND ${TEST_EXECUTABLE_NAME} --run_test=${TEST_NAME}
                     --catch_system_error=yes)
  endforeach()
endmacro()

# ==============================================================================

macro(define_object_library target)
  cmake_parse_arguments(${target}
                        ""
                        ""
                        "SOURCES;HEADERS;DEPENDENCIES;"
                        ${ARGN})

  if(CMAKE_VERSION VERSION_LESS 3.12)
    add_custom_target(${target})
    set_target_properties(${target}
                          PROPERTIES SOURCES
                                     "${${target}_SOURCES}"
                                     INTERFACE_SOURCES
                                     "${${target}_HEADERS}"
                                     LINK_LIBRARIES
                                     "${${target}_DEPENDENCIES}")
  else()
    add_library(${target} OBJECT ${${target}_SOURCES})
    target_sources(${target} INTERFACE ${${target}_HEADERS})
    target_link_libraries(${target} PUBLIC ${${target}_DEPENDENCIES})
  endif()
  list(APPEND _doc_targets ${target})
endmacro()

# ==============================================================================

macro(add_object_library_dependency
      target
      visibility
      object_library)
  if(CMAKE_VERSION VERSION_LESS 3.12)
    get_target_property(_sources ${object_library} SOURCES)
    get_target_property(_headers ${object_library} INTERFACE_SOURCES)
    get_target_property(_dependencies ${object_library} LINK_LIBRARIES)
    target_sources(${target} ${visibility} ${_sources})
    target_sources(${target} INTERFACE ${_headers})
    target_link_libraries(${target} ${visibility} ${_dependencies})
  else()
    target_link_libraries(${target} ${visibility} ${object_library})
  endif()
endmacro()

# ==============================================================================
