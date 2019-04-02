cmake_minimum_required(VERSION 3.1)
project(wsserver CXX)

set(BOOST_ROOT /opt)
set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig)
find_package(OpenSSL)
find_package(Threads)
find_package(Boost COMPONENTS system REQUIRED )

add_executable(${PROJECT_NAME} "main.cpp")
target_include_directories(${PROJECT_NAME} PRIVATE ${Boost_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${OPENSSL_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(${PROJECT_NAME} ssl)
