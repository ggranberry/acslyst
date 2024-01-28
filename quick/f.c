


#include "platform_types.h"

#include "sysdef.h"

#include "soup_outdef.h"
#include "soupheat.h"
#include "soup_out.h"
#include "heater.h"







#define MULTCONST_LOW  10
#define MULTCONST_HIGH 20




#pragma space nodp
static const int16 ConstPerf = 250;
static const int16 divConst = 0;
static int32 result;
static int16 dev;
static int16 multConst;
static int16 oldDev;
static int16 sumDev;
uint8  counter;
uint8  heaterEnable;
#pragma space none





void testme(void);
void init(void);

static void soupControl(void);


void init(void)
{
 oldDev = 0;
 sumDev = 0;
}

void testme(void)
{
  counter++;
  if (heaterEnable == ENABLE)
     {
      if ((stateCounterMCAMode > (uint16)25) && (mcaMode == (uint8)SOUP_STATE_PHASE3))
         {
          if ((uint8)LOW_SPEED_MCA_MODE_INACTIVE == lowSpeedMCAMode)
             {
              multConst = (int16)MULTCONST_HIGH;
              soupControl();
             }
          else
             {
              if (counter >= (uint8)4)
                 {multConst = (int16)MULTCONST_LOW;
                  soupControl();
                  counter = (uint8)0;
                 }
             }
         }
     }
}

void soupControl(void)
{
 int16 tmp;

 if (soupRotationTarget < (uint16)SOUP_MIN_ROTATION)
    {
     soupRotationTarget = (uint16)SOUP_MIN_ROTATION;
    }

 dev =  soupRotationTarget - soupRotationActual;

 sumDev = sumDev + dev;

 if (sumDev > 2500)
    {
     sumDev = 2500;
    }
 else
    {
     if (sumDev < -2500)
        {
         sumDev = -2500;
        }
     else
        {
          ;
        }
    }
 result = (int32)((int32)dev * ConstPerf) +
     (int32)((int32)sumDev * multConst) +
     (int32)(((int32)(dev - oldDev)) * divConst);

 oldDev = dev;

 result = result / 65536;

 tmp = soupNominalCycleTarget + (int16)result;

 if (tmp > (uint8)NOMINAL_CYCLE_MAX)
    {
     tmp = (uint8)NOMINAL_CYCLE_MAX;
    }
 if (tmp < (uint8)NOMINAL_CYCLE_MIN)
    {
     tmp = (uint8)NOMINAL_CYCLE_MIN;
    }

 soupNominalCycleTarget = (uint8)tmp;
}
