import StateMachine.State as state

print(state.fsm.current)
state.fsm.sleep()
print(state.fsm.current)
state.fsm.wakeup()
print(state.fsm.current)