import numpy as np


def print_opt_variables(prob, print_mean=False, print_values=False):
    variables = {}
    variables['obj'] = prob.driver._objs
    variables['dvs'] = prob.driver._designvars
    variables['cons'] = prob.driver._cons

    max_length = 1
    for type_ in ['obj', 'dvs', 'cons']:
        for var_name in variables[type_]:
            if len(var_name) > max_length:
                max_length = len(var_name)

    string = '{:>%s}  {:<10}  {:<8}  {:<10}  {:<10}  {:<10}  {:<10}  {:<10}   {:<10}  {:<10}  {:<10}' % (max_length + 2)

    print()
    print('-' * 40)
    for type_ in ['obj', 'dvs', 'cons']:
        print()
        print(dict(
            obj='Objective function:',
            dvs='Design variables:',
            cons='Constraints:',
        )[type_])
        print()
        print(string.format(
            'Variable',
            'Shape',
            'Active',
            'Lower',
            'Value',
            'Value',
            'Value',
            'Upper',
            'Scaler',
            'Lower',
            'Upper',
        ))
        print(string.format(
            'name',
            '',
            'size',
            '(mean)',
            '(min)',
            '(mean)',
            '(max)',
            '(mean)',
            '',
            'viol.',
            'viol.',
        ))
        total_size = 0
        for var_name in variables[type_]:
            variable = variables[type_][var_name]

            try:
                active_size = np.prod(variable['indices'].shape)
            except:
                active_size = np.prod(prob[var_name].shape)

            try:
                upper = variable['upper']
                if 'equals' in variable and variable['equals'] is not None:
                    upper = variable['equals']
                val = prob[var_name].flatten()
                if variable['scaler'] is not None:
                    val *= variable['scaler']
                violation = val[variable['indices']] - upper
                norm = np.linalg.norm(violation[violation > 0])
                size = np.prod(violation[violation > 0].shape)
                if size > 0:
                    norm /= size ** 0.5
                if norm > 1e-5:
                    upper_violation = '(%8.3e)' % norm
                else:
                    upper_violation = ' %8.3e ' % norm
            except:
                upper_violation = ''

            try:
                lower = variable['lower']
                if 'equals' in variable and variable['equals'] is not None:
                    lower = variable['equals']
                val = prob[var_name].flatten()
                if variable['scaler'] is not None:
                    val *= variable['scaler']
                violation = lower - val[variable['indices']]
                norm = np.linalg.norm(violation[violation > 0])
                size = np.prod(violation[violation > 0].shape)
                if size > 0:
                    norm /= size ** 0.5
                if norm > 1e-5:
                    lower_violation = '(%8.3e)' % norm
                else:
                    lower_violation = ' %8.3e ' % norm
            except:
                lower_violation = ''

            try:
                lower = np.mean(variable['lower'])
                if variable['scaler'] is not None:
                    lower /= variable['scaler']
                lower = '%8.3e' % lower
            except:
                lower = ''

            try:
                upper = np.mean(variable['upper'])
                if variable['scaler'] is not None:
                    upper /= variable['scaler']
                upper = '%8.3e' % upper
            except:
                upper = ''

            if variable['scaler'] is not None:
                scaler = variable['scaler']
            else:
                scaler = ''

            print(string.format(
                var_name, 
                str(prob[var_name].shape),
                str(active_size),
                str(lower),
                str('%8.3e' % np.min(prob[var_name])),
                str('%8.3e' % np.mean(prob[var_name])),
                str('%8.3e' % np.max(prob[var_name])),
                str(upper),
                str(scaler),
                str(lower_violation),
                str(upper_violation),
            ))
            total_size += active_size
            if print_values:
                print(prob[var_name])
        print(string.format(
            'Total number', 
            '',
            total_size,
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
        ))