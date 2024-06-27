# crudite

Personal project to learn more about programming and have fun.
It does not have an ending and new requirements will be added as time goes by.

## Requirements

- [x] Create a small API to manage teas
- [ ] Create a UI to interact with the Tea API using no framework

## Learnings / Thoughts

### Create a small API to manage teas

* FastAPI is an interesting web framework that fits between Django and Flask
* Designing / Building the API with TDD is easy but beware of dependencies overrides
* Choosing not to go with a database directly and using an "in memory" store makes it easier to get a working API
* I tried to use the recommended project structure with multiple modules but it was not "comfortable". So I decided to put all my tea related functions and classes in the same file