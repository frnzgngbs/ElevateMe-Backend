# BASE PATH: localhost:8000/api/

### Endpoints for User.
- `/user/` - This endpoint allows creating and querying a user.
- `/user/login/` - Login user which returns a token authentication.
- `/user/logout/` - Logout user and delete the token associated with the user.

### Endpoints for AI model.
- `/ai/two_venn/` - Prompt problem statement given two scopes.
- `/ai/three_venn/` - Prompt problem statement given three scopes.
- `/ai/potential_root/` - Prompt potential root given list of whys.
- `/ai/five_whys/` - Prompt five whys given ranked problem statement.
- `/ai/five_hmws/` - Prompt five whys given potential root problem.
- `/ai/elevator_pitch/` - Prompt elevator pitch given five How Might We's

### Endpoints for Problem Statements
- `/two_venn_ps/` - Saves Problem statement fron the Two Venn Diagram setting.
- `/three_venn_ps/` - Saves Problem statement fron the Three Venn Diagram setting.

# Endpoints for Room
- GET `/rooms/` -  Get all the rooms.
- GET `/rooms/:id/` - Get room by ID.
- GET `/rooms/:id/members/` - Get all members of a certain room.
- GET `/rooms/:id/channels/` - Get all the room's channels.
- POST `/rooms/` - Creates a room.
- PATCH - `/room/:id/` - Updates a room.

# Endpoints for Channel
- GET `/channels/` -  Get all the channel.
- GET `/channels/:id/` - Get channel by ID.
- GET `/channels/:id/members/` - Get all members of a certain channel.
- POST `/channels/` - Creates a channel.
- PATCH - `/channels/:id/` - Updates a channel.
