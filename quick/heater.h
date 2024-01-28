#ifndef __CONTROLLER_H__
#define __CONTROLLER_H__

#pragma space nodp
extern uint8 /* PC volatile */ heaterEnable;
extern uint8 /* PC volatile */ counter;
#pragma space none

extern void init(void);
extern void activate(void);
#endif
