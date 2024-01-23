## Tasks
Simulation of a triangular power grid. Three nodes, three identical lines, one generator, two consumers. We change the reactive load of one consumer and plot the phase load angles on all nodes.

Original code runs (once an environment is set up), but is difficult to scale: We want to allow for an arbitrary number of buses, connected in a circle.

## Steps
- Get the code to run
- Understand the code
- Generalize the code
- Apply best practices

1. Running environment

```bash
python -m venv .venv
source .venv/bin/activate  # For Windows, use `source .venv/Scripts/activate` instead
pip install -r requirements.txt
```

2. Add comments
2.1 (During the next steps: remove most comments, improve code)
3. Debugging (print)
4. Split code and data
5. Functions
5.1 Purity
5.2 Type hinting
5.3 help()
6. Modules
7. Tests
7.1 Test Driven Development

## TODO
- Explain network & phases
- Mention benefit of values as variables: what if you want to change two 0.1's which are different vars?
- mention OOP?
