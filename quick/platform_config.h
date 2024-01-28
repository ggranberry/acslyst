/*
 * Copyright (C) 2005-2009 Melexis N.V.
 *
 * MelexCM Software Platform
 *
 * Generated platform config header. Do not edit directly.
 *
 * 1. head is copied from platform_config_head and should be changed there.
 * 2. platform definitions can be changed over platform_confgi_mk
 * 3. tail is copied from platform_config_tail and should be changed there.
 *
 */

/* Begin head */

#ifndef PLATFORM_CONFIG_H_
#define PLATFORM_CONFIG_H_


#define NOLIN_APP 0
#define LIN13_APP 1
#define LIN20_APP 2
#define LIN21_APP 3

/* End head */


/* Begin platform definitions */
#define PRODUCT 81200
#define MLX_SIMULATOR 0
#define MLX82001 1
#define MLX82001_REV B
#define MLX82001B 1
#define FPLL_PRELIMINARY 30000UL
#define FOSC 300
#define MLX16X8 1
#define VARIANT_NAME ""
#define APP_TYPE LIN20_APP
#define ML_BAUDRATE 9600
#define HAS_LOADER 1
#define MLX_NVRAM 1
#define LOADER 0
#define __MLX_PLTF_VERSION_MAJOR__ 1
#define __MLX_PLTF_VERSION_MINOR__ 5
#define __MLX_PLTF_VERSION_REVISION__ 4
#define __MLX_PLTF_VERSION_CUSTOMER_BUILD__ 1
#define __MLX_PLTF_VERSION_INTERNAL__ 1
/*  End platform definitions */

/* Begin tail */

/*
 * Calculation of nearest possible FPLL frequency which
 * can be achieved based on requested FPLL_PRELIMINARY frequency (Chip.mk)
 * Absolute difference between FPLL and FPLL_PRELIMINARY depends on CKDIV value
 * and can be up to FOSC (usually 300 kHz) or +/-1.5% in worst case for range
 * 4.8MHz ... 30 MHz
 *
 * FOSC is used as a clock source and it is multiplied to get FPLL frequency.
 * The PLL clock multiplication factor can be modified from 64 to 127 by the
 * IO port FBDIV. Further its output can be divided by 1, 2, 3 or 4 by setting
 * the IO port CKDIV.
 * The frequency of the high speed clock is calculated as followed:
 * FPLL = FOSC * 2 * (FBDIV + 1) / (CKDIV + 1),
 * where:
 *     FPLL: PLL frequency
 *     FOSC: internal RC oscillator frequency (usually 307.2 kHz)
 *     FBDIV: 31..63 (recommended values)
 *     CKDIV: 0..3
 */

#if  (FPLL_PRELIMINARY > 30000) || (FPLL_PRELIMINARY < 4800)
#  error "Requested FPLL (FPLL_PRELIMINARY from Chip.mk) should be in range 4800 - 30000. "

#elif ( (FPLL_PRELIMINARY <= 30000) && (FPLL_PRELIMINARY > 19200) )
#  define FBDIV_VAL     (( FPLL_PRELIMINARY * 10 / 2 / FOSC + 5 ) / 10 - 1)
#  define CKDIV_VAL     0
#  define FPLL          ( 2 * FOSC * (FBDIV_VAL + 1) )

#elif ( (FPLL_PRELIMINARY <= 19200) && (FPLL_PRELIMINARY > 12900) )
#  define FBDIV_VAL     (( 2 * FPLL_PRELIMINARY * 10 / 2 / FOSC + 5 ) / 10 - 1)
#  define CKDIV_VAL     1
#  define FPLL          ( FOSC * (FBDIV_VAL + 1) )

#elif ( (FPLL_PRELIMINARY <= 12900) && (FPLL_PRELIMINARY > 9000) )
#  define FBDIV_VAL     (( 3 * FPLL_PRELIMINARY * 10 / 2 / FOSC + 5 ) / 10 - 1)
#  define CKDIV_VAL     2
#  define FPLL          (( 2 * FOSC * (FBDIV_VAL + 1) * 10 / 3 + 5 ) / 10 )

#else /* ( (FPLL_PRELIMINARY <= 9000) && (FPLL_PRELIMINARY >=4800) ) */
#  define FBDIV_VAL     (( 4 * FPLL_PRELIMINARY * 10 / 2 / FOSC + 5 ) / 10 - 1)
#  define CKDIV_VAL     3
#  define FPLL          ( 2 * FOSC * (FBDIV_VAL + 1) )
#endif /* FPLL_PRELIMINARY */


#ifndef FPLL
#error "Failed to define FPLL."
#endif /* FPLL defined */




#ifndef HAS_LOADER
#error "HAS_LOADER not defined."
#endif
#if (HAS_LOADER != 0) && (HAS_LOADER != 1)
#error "Incorrect HAS_LOADER value (should be either 0 or 1)"
#endif

#ifndef APP_TYPE
#error "APP_TYPE not defined."
#endif

#if APP_TYPE > LIN21_APP
#error "Incorrect APP_TYPE value."
#endif

#if (APP_TYPE == NOLIN_APP) && (HAS_LOADER == 0)
#define STANDALONE_LOADER 0
#define LIN_LOADER 0
#define LIN_INCLUDED 0
#define MLX4 0
//#define RAM_LOADER 0
//#define ML_FAST_BAUDRATE 100000UL // not needed
//#define MLX4_LIN_FW_BIN // not needed
#endif

#if (APP_TYPE == NOLIN_APP) && (HAS_LOADER == 1)
#define STANDALONE_LOADER 1
#define LIN_LOADER 1
#define LIN_INCLUDED 1
#define MLX4 1
//#define RAM_LOADER 0
#define ML_FAST_BAUDRATE 100000UL
#define MLX4_LIN_FW_BIN "obj/fast2b.bin"
#endif


#if (APP_TYPE != NOLIN_APP)
    // check if PLL is set to 30MHz and 300 kHz OSC is used
#if FPLL_PRELIMINARY != 30000
#error "For LIN applications please set FPLL_PRELIMINARY to 30000 in Chip.mk. If you need other values of FPLL to be used with LIN, please contact Melexis.)"
#endif

#if (FOSC != 300)
#error "For LIN applications FOSC should be 300 in Chip.mk. If you need other values of FOSC to be used with LIN, please contact Melexis.)"
#endif

#if HAS_LOADER == 0
#define STANDALONE_LOADER 0
#define LIN_LOADER 0
#define LIN_INCLUDED 1
#define MLX4 1
//#define RAM_LOADER 0
//#define ML_FAST_BAUDRATE 100000UL
#endif

#if HAS_LOADER == 1
#define STANDALONE_LOADER 0
#define LIN_LOADER 1
#define LIN_INCLUDED 1
#define MLX4 1
//#define RAM_LOADER 0
#define ML_FAST_BAUDRATE 100000UL
#endif

#endif

#if APP_TYPE == LIN21_APP
  //Single image for all LIN2.1 baud rates
  #define  MLX4_LIN_FW_BIN "obj/lin2b.bin"
#endif

#if APP_TYPE == LIN20_APP
  //Single image for all LIN2.0 baud rates
  #define  MLX4_LIN_FW_BIN "obj/lin2b.bin"
#endif

#if APP_TYPE == LIN13_APP
  #if ML_BAUDRATE == 9600
  #define MLX4_LIN_FW_BIN "obj/lin2b_v13_9600.bin"
  #elif ML_BAUDRATE == 19200
  #define MLX4_LIN_FW_BIN "obj/lin2b_v13_19200.bin"
  #else
  #error "There is no MLX4 LIN image for specified baud rate $(ML_BAUDRATE). Please contact Melexis)"
  #endif
#endif

#if LOADER == 1
#if HAS_LOADER == 0
	#error "LIN-pin loader image is NOT required for this configuration"
#endif
#endif

/* End tail */

#endif /*PLATFORM_CONFIG_H_*/
