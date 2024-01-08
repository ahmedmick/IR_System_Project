from tkinter import Label


MAIN_MENU_STEP_FORWARD_VALUE = 10
MAIN_MENU_STEP_BACKWARD_VALUE = -10

BOOLEAN_STEP_FORWARD_VALUE = 10
BOOLEAN_STEP_BACKWARD_VALUE = -10

INVERSE_STEP_FORWARD_VALUE = 10
INVERSE_STEP_BACKWARD_VALUE = -10

POSITIONAL_STEP_FORWARD_VALUE = 10
POSITIONAL_STEP_BACKWARD_VALUE = -10

VECTOR_DOCUMENT_STEP_FORWARD_VALUE = 10
VECTOR_DOCUMENT_STEP_BACKWARD_VALUE = -10

VECTOR_QUERY_STEP_FORWARD_VALUE = 10
VECTOR_QUERY_STEP_BACKWARD_VALUE = -10


def main_menu_component_motion(component, X, Y):
    for i in range(X - 100, X + 31, MAIN_MENU_STEP_FORWARD_VALUE):
        component.place(x=i, y=Y)
        component.update()
        component.after(1)
    for i in range(X + 30, X + 1, MAIN_MENU_STEP_BACKWARD_VALUE):
        component.place(x=i, y=Y)
        component.update()
        component.after(1)


def boolean_component_motion(component, X, Y):
    if isinstance(component, Label):
        for i in range(X - 100, X + 31, BOOLEAN_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X + 30, X + 1, BOOLEAN_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
    else:
        for i in range(X + 100, X - 31, BOOLEAN_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X - 32, X - 1, BOOLEAN_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)


def inverse_component_motion(component, X, Y):
    if isinstance(component, Label):
        for i in range(X - 100, X + 31, INVERSE_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X + 30, X + 1, INVERSE_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
    else:
        for i in range(X + 100, X - 31, INVERSE_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X - 32, X - 1, INVERSE_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)


def positional_component_motion(component, X, Y):
    if isinstance(component, Label):
        for i in range(X - 100, X + 31, POSITIONAL_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X + 30, X + 1, POSITIONAL_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
    else:
        for i in range(X + 100, X - 31, POSITIONAL_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X - 32, X - 1, POSITIONAL_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)


def vector_document_component_motion(component, X, Y):
    if isinstance(component, Label):
        for i in range(X - 100, X + 31, VECTOR_DOCUMENT_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X + 30, X + 1, VECTOR_DOCUMENT_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
    else:
        for i in range(X + 100, X - 31, VECTOR_DOCUMENT_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X - 32, X - 1, VECTOR_DOCUMENT_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)


def vector_query_component_motion(component, X, Y):
    if isinstance(component, Label):
        for i in range(X - 100, X + 31, VECTOR_QUERY_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X + 30, X + 1, VECTOR_QUERY_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
    else:
        for i in range(X + 100, X - 31, VECTOR_QUERY_STEP_BACKWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
        for i in range(X - 32, X - 1, VECTOR_QUERY_STEP_FORWARD_VALUE):
            component.place(x=i, y=Y)
            component.update()
            component.after(1)
