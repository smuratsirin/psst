import ipywidgets as ipyw
import traitlets as T

M = 1e10


class Generator(T.HasTraits):

    '''Generator Model'''

    name = T.CUnicode(default_value='GenCo0', help='Name of Generator (str)')
    capacity = T.CFloat(default_value=0, min=0, help='Capacity of Generator (MW)')
    noload_cost = T.CFloat(default_value=0, min=0, help='No-Load Cost of a Generator ($/hr)')
    startup_cost = T.CFloat(default_value=0, min=0, help='Startup Cost of a Generator ($/hr)')
    minimum_up_time = T.CInt(default_value=0, min=0, help='Minimum up time (hrs)')
    minimum_down_time = T.CInt(default_value=0, min=0, help='Minimum down time (hrs)')
    ramp_up_rate = T.CFloat(default_value=0, min=0, help='Ramp up rate (MW/hr)')
    ramp_down_rate = T.CFloat(default_value=0, min=0, help='Ramp down rate (MW/hr)')
    minimum_generation = T.CFloat(default_value=0, min=0, help='Minimum generation (MW)')
    generation_type = T.Enum([
        'COAL',
        'NATURALGAS',
        'WIND'
    ], default_value='COAL')
    startup_time = T.CInt(default_value=0, min=0, help='Startup time (hrs)')
    shutdown_time = T.CInt(default_value=0, min=0, help='Shutdown time (hrs)')
    initial_status = T.CBool(default_value=True, min=0, help='Initial status (bool)')
    initial_generation = T.CFloat(default_value=0, min=0, help='Initial power generation (MW)')
    inertia = T.CFloat(allow_none=True, default_value=None, min=0, help='Inertia of generator (NotImplemented)')
    droop = T.CFloat(allow_none=True, default_value=None, min=0, help='Droop of generator (NotImplemented)')

    @T.validate(
        'ramp_up_rate',
        'ramp_down_rate',
        'initial_generation'
    )
    def _less_than_capacity_check(self, proposal):
        if proposal['value'] > self.capacity:
            raise T.TraitError(
                '{class_name}().{trait_name} must be a less than or equal to {class_name}().capacity.'.format(
                    class_name=proposal['owner'].__class__.__name__,
                    trait_name=proposal['trait'].name
                )
            )
        else:
            return proposal['value']


class GeneratorView(ipyw.Box):

    model = T.Instance(Generator)

    def __init__(self, model=None, *args, **kwargs):

        if model is not None:
            self.model = model
        else:
            self.model = Generator()

        super(GeneratorView, self).__init__(*args, **kwargs)

        self._title = ipyw.HTML('Generator:')

        self._name = ipyw.Text(
            value='GenCo0',
            description='Name',
            style={'description_width': 'initial'}
        )

        self._capacity = ipyw.BoundedFloatText(
            value=self.model.capacity,
            min=0,
            max=M,
            description='Capacity (MW):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._generation_type = ipyw.Dropdown(
            value=self.model.generation_type,
            options=Generator.generation_type.values,
            description='Generation Type:',
            style={'description_width': 'initial'}
        )

        self._initial_status = ipyw.Checkbox(
            value=self.model.initial_status,
            description='Initial Status:',
            style={'description_width': 'initial'}
        )

        self._initial_generation = ipyw.BoundedFloatText(
            value=self.model.initial_generation,
            min=0,
            max=0,
            description='Initial Generation (MW):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._minimum_up_time = ipyw.BoundedFloatText(
            value=self.model.minimum_up_time,
            min=0,
            max=24,
            description='Minimum Up Time (hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._minimum_down_time = ipyw.BoundedFloatText(
            value=self.model.minimum_down_time,
            min=0,
            max=24,
            description='Minimum Down Time (hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._minimum_generation = ipyw.BoundedFloatText(
            value=self.model.minimum_generation,
            min=0,
            max=0,
            description='Minimum Generation (MW):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._noload_cost = ipyw.BoundedFloatText(
            value=self.model.noload_cost,
            min=0,
            max=M,
            description='No-Load Cost ($/hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._startup_cost = ipyw.BoundedFloatText(
            value=self.model.startup_cost,
            min=0,
            max=M,
            description='Startup Cost ($/hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._ramp_up_rate = ipyw.BoundedFloatText(
            value=self.model.ramp_up_rate,
            min=0,
            max=0,
            description='Ramp Up Rate (MW/hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._ramp_down_rate = ipyw.BoundedFloatText(
            value=self.model.ramp_down_rate,
            min=0,
            max=0,
            description='Ramp Down Rate (MW/hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._startup_time = ipyw.BoundedFloatText(
            value=self.model.startup_time,
            min=0,
            max=24,
            description='Startup Time (hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        self._shutdown_time = ipyw.BoundedFloatText(
            value=self.model.shutdown_time,
            min=0,
            max=24,
            description='Shutdown Time (hr):',
            disabled=False,
            style={'description_width': 'initial'}
        )

        children = [
            self._title,
            self._name,
            self._initial_status,
            self._generation_type,
            self._capacity,
            self._minimum_generation,
            self._initial_generation,
            self._minimum_up_time,
            self._minimum_down_time,
            self._ramp_down_rate,
            self._ramp_up_rate,
            self._startup_time,
            self._shutdown_time,
            self._noload_cost,
            self._startup_cost
        ]

        self.children = children

        T.link((self._capacity, 'value'), (self._initial_generation, 'max'), )
        T.link((self._capacity, 'value'), (self._minimum_generation, 'max'), )
        T.link((self._capacity, 'value'), (self._ramp_up_rate, 'max'), )
        T.link((self._capacity, 'value'), (self._ramp_down_rate, 'max'), )

        T.link((self.model, 'name'), (self._name, 'value'), )
        T.link((self.model, 'generation_type'), (self._generation_type, 'value'), )
        T.link((self.model, 'initial_status'), (self._initial_status, 'value'), )
        T.link((self.model, 'capacity'), (self._capacity, 'value'), )
        T.link((self.model, 'minimum_generation'), (self._minimum_generation, 'value'), )
        T.link((self.model, 'initial_generation'), (self._initial_generation, 'value'), )
        T.link((self.model, 'minimum_up_time'), (self._minimum_up_time, 'value'), )
        T.link((self.model, 'minimum_down_time'), (self._minimum_down_time, 'value'), )


class GeneratorRowView(GeneratorView):

    _model_name = T.Unicode('HBoxModel').tag(sync=True)
    _view_name = T.Unicode('HBoxView').tag(sync=True)


class GeneratorColumnView(GeneratorView):

    _model_name = T.Unicode('VBoxModel').tag(sync=True)
    _view_name = T.Unicode('VBoxView').tag(sync=True)
