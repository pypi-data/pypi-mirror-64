from logging import getLogger

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dtale.global_state as global_state
from dtale.charts.utils import ZAXIS_CHARTS
from dtale.dash_application.charts import build_chart, chart_url_params
from dtale.dash_application.layout import (bar_input_style, base_layout,
                                           build_input_options, charts_layout,
                                           get_yaxis_type_tabs,
                                           show_chart_per_group,
                                           show_input_handler,
                                           show_yaxis_ranges)
from dtale.utils import dict_merge, make_list, run_query

logger = getLogger(__name__)


class DtaleDash(dash.Dash):
    """
    Wrapper class to dash.Dash to allow for abstraction of global state used for building the default layout.
    Additional state include stylesheets, JS files and styling for github demos.
    """

    def __init__(self, *args, **kwargs):
        server = kwargs.get('server')
        kwargs['external_stylesheets'] = ['/css/main.css', '/css/dash.css']
        if server.config['GITHUB_FORK']:
            kwargs['external_stylesheets'].append('/css/github_fork.css')
        kwargs['external_scripts'] = [
            '/dash/components_bundle.js', '/dash/custom_bundle.js', '/dist/base_styles_bundle.js'
        ]

        super(DtaleDash, self).__init__(*args, **kwargs)

    def interpolate_index(self, **kwargs):
        return base_layout(self.server.config['GITHUB_FORK'], **kwargs)


def add_dash(server):
    """
    Adds dash support to main D-Tale Flask process.

    :param server: main D-Tale Flask process
    :type server: :class:`flask:flask.Flask`
    :return: server with dash added
    :rtype: :class:`flask:flask.Flask`
    """

    dash_app = DtaleDash(server=server, routes_pathname_prefix='/charts/', eager_loading=True)

    # Since we're adding callbacks to elements that don't exist in the app.layout,
    # Dash will raise an exception to warn us that we might be
    # doing something wrong.
    # In this case, we're adding the elements through a callback, so we can ignore
    # the exception.
    dash_app.config.suppress_callback_exceptions = True
    dash_app.layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='popup-content')])
    dash_app.scripts.config.serve_locally = True

    init_callbacks(dash_app)

    return dash_app.server


def get_data_id(pathname):
    """
    Parses data ID from query path (ex: 'foo/bar/1' => '1')
    """
    return pathname.split('/')[-1]


def init_callbacks(dash_app):
    """
    Dynamically adds dash callbacks to dash-wrapped flask server

    :param dash_app: flask server with dash support enabled
    :type dash_app: :class:`flask:flask.Flask`
    :return: flask server with dash callbacks added
    :rtype: :class:`flask:flask.Flask`
    """

    @dash_app.callback(
        [Output('query-data', 'data'), Output('query-input', 'style'), Output('query-input', 'title')],
        [Input('query-input', 'value')],
        [State('url', 'pathname'), State('query-data', 'data')]
    )
    def query_input(query, pathname, curr_query):
        """
        dash callback for storing valid pandas dataframe queries.  This acts as an intermediary between values typed
        by the user and values that are applied to pandas dataframes.  Most of the time what the user has typed is not
        complete and thus not a valid pandas dataframe query.

        :param query: query input
        :type query: str
        :param pathname: URL path
        :param curr_query: current valid pandas dataframe query
        :return: tuple of (query (if valid), styling for query input (if invalid input), query input title (containing
        invalid query exception information)
        :rtype: tuple of (str, str, str)
        """
        try:
            data_id = get_data_id(pathname)
            data = global_state.get_data(data_id)
            ctxt_vars = global_state.get_context_variables(data_id)
            run_query(data, query, ctxt_vars)
            return query, {'line-height': 'inherit'}, ''
        except BaseException as ex:
            return curr_query, {'line-height': 'inherit', 'background-color': 'pink'}, str(ex)

    @dash_app.callback(
        [
            Output('input-data', 'data'),
            Output('x-dropdown', 'options'),
            Output('y-single-dropdown', 'options'),
            Output('y-multi-dropdown', 'options'),
            Output('z-dropdown', 'options'),
            Output('group-dropdown', 'options'),
            Output('barsort-dropdown', 'options'),
            Output('yaxis-dropdown', 'options'),
        ],
        [
            Input('query-data', 'modified_timestamp'),
            Input('chart-tabs', 'value'),
            Input('x-dropdown', 'value'),
            Input('y-multi-dropdown', 'value'),
            Input('y-single-dropdown', 'value'),
            Input('z-dropdown', 'value'),
            Input('group-dropdown', 'value'),
            Input('agg-dropdown', 'value'),
            Input('window-input', 'value'),
            Input('rolling-comp-dropdown', 'value'),
        ],
        [State('url', 'pathname'), State('query-data', 'data')]
    )
    def input_data(_ts, chart_type, x, y_multi, y_single, z, group, agg, window, rolling_comp, pathname, query):
        """
        dash callback for maintaining chart input state and column-based dropdown options.  This will guard against
        users selecting the same column for multiple axes.
        """
        y_val = make_list(y_single if chart_type in ZAXIS_CHARTS else y_multi)
        inputs = dict(query=query, chart_type=chart_type, x=x, y=y_val, z=z, group=group, agg=agg, window=window,
                      rolling_comp=rolling_comp)
        data_id = get_data_id(pathname)
        options = build_input_options(global_state.get_data(data_id), **inputs)
        x_options, y_multi_options, y_single_options, z_options, group_options, barsort_options, yaxis_options = options
        return (
            inputs, x_options, y_single_options, y_multi_options, z_options, group_options, barsort_options,
            yaxis_options
        )

    @dash_app.callback(
        [
            Output('y-multi-input', 'style'),
            Output('y-single-input', 'style'),
            Output('z-input', 'style'),
            Output('group-input', 'style'),
            Output('rolling-inputs', 'style'),
            Output('cpg-input', 'style'),
            Output('barmode-input', 'style'),
            Output('barsort-input', 'style'),
            Output('yaxis-input', 'style')
        ],
        [Input('input-data', 'modified_timestamp')],
        [State('input-data', 'data')]
    )
    def input_toggles(_ts, inputs):
        """
        dash callback controlling showing/hiding of chart-specific inputs (for example z-axis) as well as chart
        formatting inputs (sorting for bars in bar chart, bar chart style (stacked) or y-axis ranges.
        """
        [chart_type, agg] = [inputs.get(p) for p in ['chart_type', 'agg']]
        show_input = show_input_handler(chart_type)

        y_multi_style = {'display': 'block' if show_input('y', 'multi') else 'none'}
        y_single_style = {'display': 'block' if show_input('y') else 'none'}
        z_style = {'display': 'block' if show_input('z') else 'none'}
        group_style = {'display': 'block' if show_input('group') else 'none'}
        rolling_style = {'display': 'inherit' if agg == 'rolling' else 'none'}
        cpg_style = {'display': 'block' if show_chart_per_group(**inputs) else 'none'}
        bar_style = bar_input_style(**inputs)
        yaxis_style = {'display': 'block' if show_yaxis_ranges(**inputs) else 'none'}

        return (
            y_multi_style, y_single_style, z_style, group_style, rolling_style, cpg_style, bar_style, bar_style,
            yaxis_style
        )

    @dash_app.callback(
        Output('chart-input-data', 'data'),
        [
            Input('cpg-toggle', 'on'),
            Input('barmode-dropdown', 'value'),
            Input('barsort-dropdown', 'value'),
        ]
    )
    def chart_input_data(cpg, barmode, barsort):
        """
        dash callback for maintaining selections in chart-formatting inputs
            - chart per group flag
            - bar chart mode
            - bar chart sorting
        """
        return dict(cpg=cpg, barmode=barmode, barsort=barsort)

    @dash_app.callback(
        [
            Output('chart-content', 'children'),
            Output('last-chart-input-data', 'data'),
            Output('range-data', 'data'),
            Output('chart-code', 'value'),
            Output('yaxis-type', 'children'),
        ],
        # Since we use the data prop in an output,
        # we cannot get the initial data on load with the data prop.
        # To counter this, you can use the modified_timestamp
        # as Input and the data as State.
        # This limitation is due to the initial None callbacks
        # https://github.com/plotly/dash-renderer/pull/81
        [
            Input('input-data', 'modified_timestamp'),
            Input('chart-input-data', 'modified_timestamp'),
            Input('yaxis-data', 'modified_timestamp'),
        ],
        [
            State('url', 'pathname'),
            State('input-data', 'data'),
            State('chart-input-data', 'data'),
            State('yaxis-data', 'data'),
            State('last-chart-input-data', 'data')
        ]
    )
    def on_data(_ts1, _ts2, _ts3, pathname, inputs, chart_inputs, yaxis_data, last_chart_inputs):
        """
        dash callback controlling the building of dash charts
        """
        all_inputs = dict_merge(inputs, chart_inputs, dict(yaxis=yaxis_data or {}))
        if all_inputs == last_chart_inputs:
            raise PreventUpdate
        charts, range_data, code = build_chart(get_data_id(pathname), **all_inputs)
        return charts, all_inputs, range_data, code, get_yaxis_type_tabs(make_list(inputs.get('y') or []))

    def get_default_range(range_data, y, max=False):
        if max:
            return next(iter(sorted([range_data[y2] for y2 in y if y2 in range_data], reverse=True)), None)
        return next(iter(sorted([range_data[y2] for y2 in y if y2 in range_data])), None)

    @dash_app.callback(
        [
            Output('yaxis-min-input', 'value'),
            Output('yaxis-max-input', 'value'),
            Output('yaxis-dropdown', 'style'),
            Output('yaxis-min-label', 'style'),
            Output('yaxis-min-input', 'style'),
            Output('yaxis-max-label', 'style'),
            Output('yaxis-max-input', 'style'),
            Output('yaxis-type-div', 'style'),
        ],
        [Input('yaxis-type', 'value'), Input('yaxis-dropdown', 'value')],
        [State('input-data', 'data'), State('yaxis-data', 'data'), State('range-data', 'data')]
    )
    def yaxis_min_max_values(yaxis_type, yaxis, inputs, yaxis_inputs, range_data):
        """
        dash callback controlling values for selected y-axis in y-axis range editor
        """
        y = make_list(inputs.get('y'))
        dd_style = dict(display='block' if yaxis_type == 'multi' and len(y) > 1 else 'none')
        type_style = {'borderRadius': '0 0.25rem 0.25rem 0'} if yaxis_type == 'default' else None
        min_max_style = 'none' if (yaxis_type == 'default') or (yaxis_type == 'multi' and yaxis is None) else 'block'
        label_style = dict(display=min_max_style)
        input_style = {'lineHeight': 'inherit', 'display': min_max_style}
        curr_min, curr_max = (None, None)
        range_min, range_max = ((range_data or {}).get(p) or {} for p in ['min', 'max'])
        if yaxis:
            curr_vals = (yaxis_inputs or {}).get('data', {}).get(yaxis) or {}
            curr_min = curr_vals.get('min') or range_min.get(yaxis)
            curr_max = curr_vals.get('max') or range_max.get(yaxis)
        elif yaxis_type == 'single':
            curr_vals = (yaxis_inputs or {}).get('data', {}).get('all') or {}
            curr_min = curr_vals.get('min')
            if curr_min is None:
                curr_min = get_default_range(range_min, y)
            curr_max = curr_vals.get('max')
            if curr_max is None:
                curr_max = get_default_range(range_max, y, max=True)
        return curr_min, curr_max, dd_style, label_style, input_style, label_style, input_style, type_style

    @dash_app.callback(
        Output('yaxis-data', 'data'),
        [Input('yaxis-type', 'value'), Input('yaxis-min-input', 'value'), Input('yaxis-max-input', 'value')],
        [
            State('yaxis-dropdown', 'value'),
            State('yaxis-data', 'data'),
            State('range-data', 'data'),
            State('input-data', 'data')
        ]
    )
    def update_yaxis_data(yaxis_type, yaxis_min, yaxis_max, yaxis, yaxis_data, range_data, inputs):
        """
        dash callback controlling updates to y-axis range state
        """
        yaxis_data = yaxis_data or dict(data={})
        yaxis_data['type'] = yaxis_type
        yaxis_name = 'all' if yaxis_type == 'single' else yaxis
        if yaxis_name == 'all':
            y = make_list(inputs.get('y'))
            mins = range_data.get('min', {})
            maxs = range_data.get('max', {})
            range_min = get_default_range(mins, y)
            range_max = get_default_range(maxs, y, max=True)
        elif yaxis is None:
            raise PreventUpdate
        else:
            range_min, range_max = (range_data[p].get(yaxis_name) for p in ['min', 'max'])

        if yaxis_name in yaxis_data['data']:
            if (yaxis_min, yaxis_max) == (range_min, range_max):
                del yaxis_data['data'][yaxis_name]
            else:
                yaxis_data['data'][yaxis_name] = dict(min=yaxis_min, max=yaxis_max)
        else:
            if (yaxis_min, yaxis_max) != (range_min, range_max):
                yaxis_data['data'][yaxis_name] = dict(min=yaxis_min, max=yaxis_max)
        return yaxis_data

    @dash_app.callback(
        Output('popup-content', 'children'),
        [Input('url', 'modified_timestamp')],
        [State('url', 'pathname'), State('url', 'search')])
    def display_page(_ts, pathname, search):
        """
        dash callback which gets called on initial load of each dash page (main & popup)
        """
        dash_app.config.suppress_callback_exceptions = False
        params = chart_url_params(search)
        data_id = get_data_id(pathname)
        df = global_state.get_data(data_id)
        settings = global_state.get_settings(data_id) or {}
        return charts_layout(df, settings, **params)
