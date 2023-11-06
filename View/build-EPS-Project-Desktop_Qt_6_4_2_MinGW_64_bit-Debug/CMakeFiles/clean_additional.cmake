# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\EPS-Project_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\EPS-Project_autogen.dir\\ParseCache.txt"
  "EPS-Project_autogen"
  )
endif()
