add_boost_test(${CMAKE_CURRENT_LIST_DIR}/xsimd_fallback_test.cpp)

add_boost_test(${CMAKE_CURRENT_LIST_DIR}/stabilizer_simulator_test.cpp)
target_include_directories(stabilizer_simulator_test
                           PRIVATE ${PYBIND11_INCLUDE_DIR}
                           PRIVATE ${pybind11_INCLUDE_DIR}
                           PRIVATE ${PYTHON_INCLUDE_DIRS})

add_avx2_to_target(stabilizer_simulator_test)

find_package(Threads REQUIRED)
target_link_libraries(stabilizer_simulator_test PRIVATE Threads::Threads)

if(_found_projectq)
  target_link_libraries(stabilizer_simulator_test PRIVATE ${xsimd_tgt})
  target_compile_definitions(stabilizer_simulator_test
                             PRIVATE
                             -DHAS_PYTHON
                             -DPYTHON_EXECUTABLE="${Python_EXECUTABLE}")
endif()
