# BASE PATH: localhost:8000/api/

### This endpoints is related to the User.
- `/user/` - This endpoint allows creating and querying a user.
- `/user/login/` - Login user which returns a token authentication.
- `/user/logout/` - Logout user and delete the token associated with the user.

### This endpoints is for the AI model.
- `/ai/two_venn/` - Prompt problem statement given two scopes.
- `/ai/three_venn/` - Prompt problem statement given three scopes.
- `/ai/potential_root/` - Prompt potential root given list of whys.
- `/ai/five_whys/` - Prompt five whys given ranked problem statement.
- `/ai/five_hmws/` - Prompt five whys given potential root problem.
- `/ai/elevator_pitch/` - Prompt elevator pitch given five How Might We's

### This endpoints is for the saving of Problem Statements
- `/two_venn_ps/` - Saves Problem statement fron the Two Venn Diagram setting.
- `/three_venn_ps/` - Saves Problem statement fron the Three Venn Diagram setting.
