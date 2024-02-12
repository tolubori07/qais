from sympy import symbols, Eq, solve

def beam_analysis(number_of_supports, number_of_internal_joints, spans_data):
    number_of_nodes = number_of_supports + number_of_internal_joints
    number_of_spans = number_of_nodes - 1

    class Node:
        def __init__(self, settlement, angular_displacement, equilibrium_equation, node_reaction):
            self.settlement = settlement
            self.angular_displacement = angular_displacement
            self.equilibrium_equation = equilibrium_equation
            self.node_reaction = node_reaction

    beam_nodes = []
    settlement_variable = 0
    angular_displacement_variable = 0
    equilibrium_equation_variable = ""
    node_reaction_variable = 0
    for i in range(number_of_nodes):
        beam_nodes.append("")
        beam_nodes[i] = Node(settlement_variable, angular_displacement_variable, equilibrium_equation_variable,
                             node_reaction_variable)

    list_of_unknown_angular_displacements = []
    first_node = "A"
    for i in range(number_of_nodes):
        if i != 0 and i != number_of_nodes - 1:
            beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
            list_of_unknown_angular_displacements.append(beam_nodes[i].angular_displacement)
        else:
            beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
            beam_nodes[i].angular_displacement = 0

        first_node = chr(ord(first_node) + 1)

    class Span:
        def __init__(self, left_fem, right_fem, span_length, load, loading_condition, cord_rotation, left_moment,
                     right_moment, left_slope_deflection_equation, right_slope_deflection_equation,
                     reaction_at_left_node_on_span, reaction_at_right_node_on_span, span_a_value):
            self.left_fem = left_fem
            self.right_fem = right_fem
            self.span_length = span_length
            self.load = load
            self.loading_condition = loading_condition
            self.cord_rotation = cord_rotation
            self.left_moment = left_moment
            self.right_moment = right_moment
            self.left_slope_deflection_equation = left_slope_deflection_equation
            self.right_slope_deflection_equation = right_slope_deflection_equation
            self.reaction_at_left_node_on_span = reaction_at_left_node_on_span
            self.reaction_at_right_node_on_span = reaction_at_right_node_on_span
            self.span_a_value = span_a_value

    beam_spans = []
    left_fem_variable = 1
    right_fem_variable = 1
    span_length_variable = 1
    load_variable = 1
    loading_condition_variable = ""
    cord_rotation_variable = 1
    left_moment_variable = 1
    right_moment_variable = 1
    left_slope_deflection_equation_variable = ""
    right_slope_deflection_equation_variable = ""
    reaction_at_left_node_on_span_variable = 1
    reaction_at_right_node_on_span_variable = 1
    span_a_value_variable = 1

    for i in range(number_of_spans):
        beam_spans.append("")
        beam_spans[i] = Span(left_fem_variable, right_fem_variable, span_length_variable, load_variable,
                             loading_condition_variable, cord_rotation_variable, left_moment_variable,
                             right_moment_variable, left_slope_deflection_equation_variable,
                             right_slope_deflection_equation_variable, reaction_at_left_node_on_span_variable,
                             reaction_at_right_node_on_span_variable, span_a_value_variable)

    length_of_beam = 0
    for i, span_data in enumerate(spans_data):
        beam_spans[i].loading_condition = span_data['loading_condition']
        beam_spans[i].span_length = span_data['span_length']
        beam_spans[i].load = span_data['load']

        length_of_beam += beam_spans[i].span_length

        if beam_spans[i].loading_condition == 'P_C':
            beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length) / 8
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'P_X':
            beam_spans[i].span_a_value = span_data['span_a_value']
            a = beam_spans[i].span_a_value
            b = beam_spans[i].span_length - a
            beam_spans[i].right_fem = (beam_spans[i].load * b * a * a) / (beam_spans[i].span_length * beam_spans[i].span_length)
            beam_spans[i].left_fem = (beam_spans[i].load * b * b * a) / (beam_spans[i].span_length * beam_spans[i].span_length)

           elif beam_spans[i].loading_condition == 'P_C_2':
        beam_spans[i].right_fem = (2 * beam_spans[i].load * beam_spans[i].span_length) / 9
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

    elif beam_spans[i].loading_condition == 'P_C_3':
        beam_spans[i].right_fem = (15 * beam_spans[i].load * beam_spans[i].span_length) / 48
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

    elif beam_spans[i].loading_condition == 'UDL':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 12
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

    elif beam_spans[i].loading_condition == 'UDL/2_R':
        beam_spans[i].right_fem = (11 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[
            i].span_length) / 192
        beam_spans[i].left_fem = -1 * (5 * beam_spans[i].load * beam_spans[i].span_length *
                                       beam_spans[i].span_length) / 192

    elif beam_spans[i].loading_condition == 'UDL/2_L':
        beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 192
        beam_spans[i].left_fem = -1 * (11 * beam_spans[i].load * beam_spans[i].span_length *
                                       beam_spans[i].span_length) / 192

    elif beam_spans[i].loading_condition == 'VDL_R':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
        beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30

    elif beam_spans[i].loading_condition == 'VDL_L':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20

    elif beam_spans[i].loading_condition == 'VDL_C':
        beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 96
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

    elif beam_spans[i].loading_condition == "none":
        beam_spans[i].right_fem = 0
        beam_spans[i].left_fem = 0
        print(f"No loading on span {i+1}")

    coordinates = []
    current_length = 0
    for i in range(number_of_spans):
        span_length = beam_spans[i].span_length
        while current_length < span_length and len(coordinates) < 20:
            coordinates.append(current_length)
            current_length += length_of_beam / 20

    return coordinates

# Example usage:
# coordinates = beam_analysis(number_of_supports, number_of_internal_joints, spans_data)
