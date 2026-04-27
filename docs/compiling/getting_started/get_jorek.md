# How to obtain the JOREK source code with git

## The ITER git platform

- Request an account for the ITER platform [via e-mail](mailto:admin@jorek.eu).
- When this is set up, request access to the JOREK code repository [via this link](https://jira.iter.org/servicedesk/customer/portal/1/create/257)
- Create an ssh keypair ([help](https://confluence.atlassian.com/display/STASH/Creating+SSH+keys))
  - Run the command `ssh-keygen -t rsa -C "<key identifier>"`
  - You will be prompted for a location to save your key. Be careful not to overwrite any existing keys that you still need!
  - You can add a password for an additional layer of security (encrypting your private key file) or proceed without a password. Push Enter when prompted for a password if you don't want to add a password.
- Upload your public ssh key: [https://git.iter.org/plugins/servlet/ssh/account/keys](https://git.iter.org/plugins/servlet/ssh/account/keys)
  - The public key is stored in the `.pub` file.
  - The `.pub` file is a regular text file. You will need to copy its contents into the web form that you get after clicking "Add key".

- You can now **browse the repository online** at [https://git.iter.org/projects/STAB/repos/jorek/browse](https://git.iter.org/projects/STAB/repos/jorek/browse) — you may need to authenticate twice the first time: once to the ITER intranet and once to gain access to JOREK (link in top right-hand corner).
- The code is automatically compiled and **non-regression tests** are executed every time changes are pushed: <https://ci.iter.org/browse/STAB-JOREK> (see also the links from the green ticks in the Git web front-end: <https://git.iter.org/projects/STAB/repos/jorek/branches>).
- **Issues** (trouble tickets) are handled using JIRA (<https://jira.iter.org/browse/IMAS>) and you should feel free to create new issues associated with JOREK (selected from the drop-down list of components) if you have any problems or suggestions. You can ignore the options associated with resource estimates and sprints.

*We would like to thank ITER for hosting JOREK on their platform, especially Simon Pinches and Guido Huijsmans.*

## Get the code from the ITER platform

- **Request an account for the ITER platform** if you don't already have it (see above)
- **Clone the JOREK repository**:

```bash
git clone ssh://git@git.iter.org/stab/jorek.git
```

- [ITER Integrated Modeling Development Guide (.docx)](https://portal.iter.org/departments/POP/CM/IMAS/IM%20Development%20Guide.docx)
- Help with git: [http://git-scm.com/doc/](http://git-scm.com/doc/), especially the [Pro Git book](http://git-scm.com/book/en/v2)

## Next Steps

- [**Compiling the code**](compiling.md)
- [**Running the code**](running.md)
- **Information about development with git and our coding guidelines** **(to do: page to be created)**
