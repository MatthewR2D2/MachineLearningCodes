import StateMachine.State as my_state


def askUser(state):
    task = input("What should I do")

    if task == "wake":
        if state.fsm.current == "awake":
            print("All ready awake")
        else:
            state.fsm.wakeup()
        print(state.fsm.current)
        askUser(state)
    elif task == "sleep":
        if state.fsm.current == "sleeping":
            print("All ready sleeping")
        else:
            state.fsm.sleep()
        print(state.fsm.current)
        askUser(state)
    else:
        pass



print("Starting")

askUser(my_state)
print("Ending")






