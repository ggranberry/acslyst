#ifndef __SYSDEF_H__
#define __SYSDEF_H__

#define DISABLE 0
#define ENABLE  1

#define PWM_30kHz 30
#define PWM_20kHz 20
#define PWM_17kHz 17
#define PWM_PERIOD_FRQUENCY  PWM_20kHz

#define TIMER_RESOLUTION 0.5212

#define CONVERSION_FACTOR_RPM_2_TIMER_TICKS 60000000 / (NUMBER_OF_POLE_PAIRS * 6 * TIMER_RESOLUTION)
#define CONVERSION_FACTOR_TIMER_TICKS_2_RPM 60000000 / (NUMBER_OF_POLE_PAIRS * 6 * TIMER_RESOLUTION)

#define NUMBER_OF_SINE_STEPS   48
#define NUMBER_OF_MOTOR_STATES 6
#define NUMBER_OF_SINE_STEPS_PER_STATE (NUMBER_OF_SINE_STEPS / NUMBER_OF_MOTOR_STATES) 

#define BLDC_MODE_BIPOLAR      1
#define BLDC_MODE_TRIPOLAR     2
#define BLDC_MODE_SENSOR_BASED 3
#define BLDC_SENSOR_LESS   1
#define BLDC_SENSOR_BASED  2
#define RAMP               2
#define SENSOR             3

#define BLDC_MODE   BLDC_MODE_TRIPOLAR
#define BLDC_SENSOR BLDC_SENSOR_LESS
#define START_UP_BEHAVIOR RAMP

#define NO_INTERFACE  0
#define LIN_INTERFACE 1
#define CAN_INTERFACE 2
#define PWM_INTERFACE 3

#define COMMUNICATION_INTERFACE    LIN_INTERFACE

#define PID_CONTROLLER ENABLE
#if PID_CONTROLLER != ENABLE
 #define PID_CONTROLLER DISABLE
#endif

#define WATCHDOG_TIMEOUT      200
#define DIGITAL_WATCHDOG      ENABLE

#define ALIGNMENT_TIME_MS                 200
#define ALIGNMENT_DUTY_CYCLE              0x30
#define ROTOR_ALIGN_WITH_SENSED_POSITION  DISABLE

#if BLDC_MODE == BLDC_MODE_BIPOLAR	   
 #define TRI_PHASE_MODE ENABLE
#endif

#endif