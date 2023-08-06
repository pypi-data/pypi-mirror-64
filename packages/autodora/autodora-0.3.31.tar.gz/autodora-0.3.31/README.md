# autodora [![Build Status](https://travis-ci.org/samuelkolb/autodora.svg?branch=master)](https://travis-ci.org/samuelkolb/autodora)
autodora is a framework to help you:
1. setup experiments
2. running them for multiple parameters
3. storing the results
4. exploring the results

The aim of this package is to make these steps as easy and integrated as possible.

## Installation

    pip install autodora
    
Experiments can be tracked using observers. Specialized observers may require optional packages to function that are
not included by default (because you might not need them).

### Telegram observer

    pip install autodora[telegram]
    
In order to use the observer you have to set the environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

**Example usage**

    export TELEGRAM_BOT_TOKEN="<your-bot-token>"
    export TELEGRAM_CHAT_ID="<your-chat-id>"
    pytest


## Using autodora
Consider the problem of computing the product of two numbers given in a string like this: `"0.1 x 0.3"`.
The heavy-lifting of this computation is performed by a function `multiply`:

    def multiply(x, y):
        return x * y
        
### Setting up
We start off by describing the experiment in a file called `product_experiment.py`:

    class ProductExperiment(Experiment):
        input = Parameter(str, "0.0x0.0", "The input values to be multiplied (e.g. 0.2x10)")
        product = Result(float, description="Computed product")
    
        @derived(cache=True)
        def derived_x(self):
            return float(self.get(self.input).split("x")[0])
    
        @derived(cache=True)
        def derived_y(self):
            return float(self.get(self.input).split("x")[1])
    
        def run_internal(self):
            x, y = self.get("x"), self.get("y")
            result = multiply(x, y)
            self["product"] = result
    
    
    ProductExperiment.enable_cli()



#### Describing parameters

        ...
        input = Parameter(str, "0.0x0.0", "The input values to be multiplied (e.g. 0.2x10)")
        ...

The first step is to describe the parameters of the experiment, the name is taken from the variable you assign them to,
other than that have to specify the type and optionally a default value and description of the parameter.

While this is a powerful and easy way to set up parameters, you can also add them in the constructor:

    class ProductExperiment(Experiment):
        def __init__(self, group, storage=None, identifier=None):
            super().__init__(group, storage=None, identifier=None)
            self.parameters.add_parameter("complicated.name", datetime, None, "Description")


#### Describing results

        ...
        product = Result(float, description="Computed product")
        ...

Similar to the parameters, we specify expected results. The Result class is identical to the Parameter class in all but
name, it only serves to indicate that you are trying to assign a result.


#### Computing derived features

        ...
        @derived(cache=True)
        def derived_x(self):
            return float(self.get(self.input).split("x")[0])
    
        @derived(cache=True)
        def derived_y(self):
            return float(self.get(self.input).split("x")[1])
        ...
   
Derived features are computed from other values (or complex computation chains) and can be marked for caching to avoid
computing them over and over again: when the experiment is saved to storage, those features will be saved with the
experiment.

You can build derived features using the derived decorator, which internally builds a `Derived object` and saves it in
the `experiment.derived_callbacks (Dict[str, Derived])` dictionary. Again, you can do this in the constructor, too.
If the decorated function is called `derived_<name>`, it will be shortened to just `<name>`.

Derived features can be accessed by calling `experiment["name"]` or `experiment[""derived.name"]` to disambiguate
if there are other parameters or results with the same name.


#### Running the experiment

        ...
        def run_internal(self):
            x, y = self.get("x"), self.get("y")
            result = multiply(x, y)
            self["product"] = result
        ...

When `experiment.run()` is called, it internally calls the `run_internal` method, which is responsible for running the
actual experiment. In this case, it fetches the (derived) parameters, computes the result and stores it.


#### Enabling the command line interface

    ...
    ProductExperiment.enable_cli()
    
The `enable_cli` class method, not surprisingly, enables the current file to be run from command line.
This enables several key features:
- Making the experiment executable by command line (for internal and external use)
- Allowing you to manage (plot, list, ...) experiments of this type from command line

### Specifying trajectories

TODO
