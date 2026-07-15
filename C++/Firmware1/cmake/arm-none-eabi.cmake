set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(ARM_TOOLCHAIN_BIN "C:/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/14.2 rel1/bin" CACHE PATH "GNU Arm Embedded Toolchain bin directory")

set(CMAKE_C_COMPILER "${ARM_TOOLCHAIN_BIN}/arm-none-eabi-gcc.exe")
set(CMAKE_ASM_COMPILER "${ARM_TOOLCHAIN_BIN}/arm-none-eabi-gcc.exe")
set(CMAKE_OBJCOPY "${ARM_TOOLCHAIN_BIN}/arm-none-eabi-objcopy.exe")
set(CMAKE_SIZE "${ARM_TOOLCHAIN_BIN}/arm-none-eabi-size.exe")

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
