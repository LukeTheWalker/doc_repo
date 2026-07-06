---
title: "Coding Guidelines"
nav_order: 2
parent: "Code Development"
layout: default
render_with_liquid: false
---

# Coding Guidelines

- See also [**Committing Guidelines**](development_workflow) 
- See also [**Overview Slides by Matthias**](assets/develop/2021-10-mhoelzl-development-workflow.pdf)

## How the source code should look

- **implicit none statement:**
  - Each subroutine or module must have an "implicit none" statement.

- **external functions**
  - The use of modules is recommended. Should you want to use external functions, be sure to set `real*8, external :: funcname` to allow dependency generation to work properly. In that case the explicit specification  of an interface is recommended

- **Naming**:
  - Please use self-explanatory names for subroutines, functions, or variables whenever possible.
  - Please use the same name for the filename and the program unit in the file (case-sensitive) which is to be used outside the file (it follows that every file should have only one such program unit).
    - The build system requires program unit (module, subroutine, function, program) names to equal the filename.
    - Dependencies will only correctly find dependencies if the filename equals the program unit name.

- **Indentation**:
  - Inside each program, routine, function, if-clause, for-loop, etc, an **indentation of two spaces** is used
  - Please use blanks and **do not use tab symbols** (except for the Makefile, of course)

- **Alignment**:
  - Please align several commands of a similar structure in a way that makes them more readable, e.g., by aligning the "=" signs.

- **Comments**:
  - Comments should be put wherever the code is not self-explanatory
  - Especially, there should be a comment at the head of each subroutine describing its purpose
  - Please describe each input/output parameter if it is not self explanatory
  - For blocks of commands that belong together and also for longer loops, a short explanation is often very useful. Such blocks can be separated by a blank line to make the code more readable
  - If an implementation is not working in certain cases, please put a warning as a comment.
  - Please follow the form of the comments given below

- **Long Lines**:
  - Lines that are longer than 132 characters should be split into several lines by putting an "&" sign at the end of the first line and continuing the statement in the next line with an indentation of two extra spaces. In case it improves readability, breaking the line earlier can be useful.

- **Intent Statements**:
  - Please put each parameter of a subroutine or function into a separate line specifying whether the parameter is an input parameter (`"intent(in)"`), an output parameter (`"intent(out)"`) or both (`"intent(inout)"`) and add an explanation for it as a comment
  - In case input parameters are really self-explanatory, several of them can be put into the same line without a comment

- **Specific end statements**:
  - Each `end` statement should be as precise as possible: "end do", "end if", "end subroutine test", ...
  - Long loops or if-clauses should be given an explicit unique and readable name:

```fortran
loop_over_nodes:do i = 1, n_nodes
  ... ! Lots of code inside this loop
end do loop_over_nodes
```

- **Opening Files**:
  - Each `open` statement should contain the `action` and `status` parameters. Typically, `status` takes the values "old" (existing file), "new" (create file), or "replace" (overwrite file). For `action`, the values "read", "write" and "readwrite" are possible. Prefer "newunit=" for unit number selection.

### Example:

```fortran
  !> Put a short description for the routine in a single line.
  !! 
  !! If necessary, you can add a detailed explanation running over several lines
  !! like this.
  !! *** WARNING*** Please put a warning in case the routine does not work under certain conditions.
  subroutine print_grid_info(element_list, node_list, verbose)
    
    implicit none
    
    ! --- Routine parameters
    type(type_element_list), intent(in) :: element_list
    type(type_node_list),    intent(in) :: node_list
    logical,                 intent(in) :: verbose       !< Describe routine parameters if necessary
    
    ! --- Local variables
    type(type_node) :: node_i
    integer         :: i, j
    
    ! --- Print information about the grid nodes.
    do i = 1, node_list%n_nodes
      node_i = node_list%node(i)
      write(*,*) '...'
      if ( verbose ) then
        write(*,*) '...'
      end if
    end do ! (i = 1, node_list%n_nodes)
    ! in case of long loops, a comment might be useful to indicate which loop ends here
    
    ! --- Print information about the grid elements.
    write(*,*) '...'
    do j = 1, element_list%n_elements
      write(*,*) '...'
    end do
    
    write(*,*) element_list%n_elements, element_list%n_elements, element_list%n_elements,              &
      element_list%n_elements ! Line split after 100 characters and continued with extra indentation
    
  end subroutine print_grid_info
```


