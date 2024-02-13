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
        beam_spans[i].loading_condition = span_data['loadingCondition']
        beam_spans[i].span_length = int(span_data['spanLength'])
        beam_spans[i].load = span_data['load']

        length_of_beam += beam_spans[i].span_length

        if beam_spans[i].loading_condition == 'P_C':
            beam_spans[i].right_fem = float(beam_spans[i].load * beam_spans[i].span_length) / 8
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'P_X':
            beam_spans[i].span_a_value = span_data['span_a_value']
            a = beam_spans[i].span_a_value
            b = beam_spans[i].span_length - a
            beam_spans[i].right_fem = int((beam_spans[i].load * b * a * a) / (beam_spans[i].span_length * beam_spans[i].span_length))
            beam_spans[i].left_fem = int((beam_spans[i].load * b * b * a) / (beam_spans[i].span_length * beam_spans[i].span_length))

        elif beam_spans[i].loading_condition == 'P_C_2':
            beam_spans[i].right_fem = float(2 * beam_spans[i].load * beam_spans[i].span_length) / 9
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'P_C_3':
            beam_spans[i].right_fem = float((15 * beam_spans[i].load * beam_spans[i].span_length)) / 48
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'UDL':
            beam_spans[i].right_fem = int((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 12
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'UDL/2_R':
            beam_spans[i].right_fem = float((11 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 192
            beam_spans[i].left_fem = float(-1 * (float(5 * beam_spans[i].load) * float(beam_spans[i].span_length) * float(beam_spans[i].span_length))) / 192

        elif beam_spans[i].loading_condition == 'UDL/2_L':
            beam_spans[i].right_fem = float((5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 192
            beam_spans[i].left_fem = -1 * (11 * float(beam_spans[i].load * beam_spans[i].span_length *
                                       beam_spans[i].span_length)) / 192

        elif beam_spans[i].loading_condition == 'VDL_R':
            beam_spans[i].right_fem = float((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 20
            beam_spans[i].left_fem = -1 * (float(beam_spans[i].load) * float(beam_spans[i].span_length) * float(beam_spans[i].span_length)) / 30

        elif beam_spans[i].loading_condition == 'VDL_L':
            beam_spans[i].right_fem = float((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 30
            beam_spans[i].left_fem = float(-1 * float((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length))) / 20

        elif beam_spans[i].loading_condition == 'VDL_C':
            beam_spans[i].right_fem = float((5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 96
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == "none":
            beam_spans[i].right_fem = 0
            beam_spans[i].left_fem = 0
            print(f"No loading on span {i+1}")

    list_of_end_moments = []
    left_end = "a"
    right_end = "b"
    for i in range(number_of_spans):
        beam_spans[i].left_moment, beam_spans[i].right_moment = symbols(f"M{left_end}{right_end} M{right_end}{left_end}")
        left_end = chr(ord(left_end) + 1)
        right_end = chr(ord(right_end) + 1)
        list_of_end_moments.append(beam_spans[i].left_moment)
        list_of_end_moments.append(beam_spans[i].right_moment)

    coordinates = []
    current_length = 0
    for i in range(number_of_spans):
        span_length = beam_spans[i].span_length
        while current_length < span_length and len(coordinates) < 20:
            coordinates.append(current_length)
            current_length += length_of_beam / 20
    position_along_beam = [0]
    shear_forces = [0]
    sf = 0
    for i in range(number_of_spans):
        x = 0
        sf += beam_nodes[i].node_reaction
        position_along_beam.append(x)
        shear_forces.append(sf)
        if beam_spans[i].loading_condition == "P_C":
            x = beam_spans[i].span_length/2
            while i != 0:
                x += beam_spans[i-1].span_length
                i -= 1
            sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)
        elif beam_spans[i].loading_condition == "P_X":
            a = beam_spans[i].span_a_value
            x = beam_spans[i].span_length - a
            while i != 0:
                x += beam_spans[i-1].span_length
                i -= 1
            sf -= beam_spans[i].load

            position_along_beam.append(x)
            shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "P_C_2":
            x = beam_spans[i].span_length - beam_spans[i].span_length/3
            while i != 0:
                x += beam_spans[i-1].span_length
                i -= 1
            sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)

            x = beam_spans[i].span_length - (2*beam_spans[i].span_length)/3
            while i != 0:
                x += beam_spans[i-1].span_length
                i -= 1
            sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "P_C_3":
            x = beam_spans[i].span_length - beam_spans[i].span_length / 4
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1
                sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)
            x = beam_spans[i].span_length - (2 * beam_spans[i].span_length) / 4
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1
            sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)

            x = beam_spans[i].span_length - (3 * beam_spans[i].span_length) / 4
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1
            sf -= float(beam_spans[i].load)
            position_along_beam.append(x)
            shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "UDL":
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1

            for u in range(beam_spans[i].span_length):
                x += u
                sf -= int(beam_spans[i].load) * u
                position_along_beam.append(x)
                shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "UDL/2_R":
            x = beam_spans[i].span_length/2
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1

            for u in range(beam_spans[i].span_length):
                x += u
                sf -= (float(beam_spans[i].load) * u)
                position_along_beam.append(x)
                shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "UDL/2_L":
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1

            for u in range(int(round(beam_spans[i].span_length)/2)):
                x += u
                sf -= int(beam_spans[i].load) * u
                position_along_beam.append(x)
                shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "VDL_R":
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1

            for u in range(beam_spans[i].span_length):
                x += u
                sf -= (float(beam_spans[i].load)* u * u) / (2*float(beam_spans[i].span_length))
                position_along_beam.append(x)
                shear_forces.append(sf)

        elif beam_spans[i].loading_condition == "VDL_L":
            while i != 0:
                x += beam_spans[i - 1].span_length
                i -= 1

            for u in range(beam_spans[i].span_length):
                x += u
                sf -= ((int(beam_spans[i].load) * u)/beam_spans[i].span_length) * (2 - (u/int(beam_spans[i].span_length)))
                position_along_beam.append(x)
                shear_forces.append(sf)

    if i == number_of_spans - 1:
        position_along_beam.append(length_of_beam)
        sf += beam_nodes[i+1].node_reaction
        shear_forces.append(sf)


    return position_along_beam, shear_forces

# Example usage:
# coordinates = beam_analysis(number_of_supports, number_of_internal_joints, spans_data)
# from sympy import symbols, Eq, solve

# def beam_analysis(number_of_supports, number_of_internal_joints, spans_data):
#     number_of_nodes = number_of_supports + number_of_internal_joints
#     number_of_spans = number_of_nodes - 1

#     class Node:
#         def __init__(self, settlement, angular_displacement, equilibrium_equation, node_reaction):
#             self.settlement = settlement
#             self.angular_displacement = angular_displacement
#             self.equilibrium_equation = equilibrium_equation
#             self.node_reaction = node_reaction

#     beam_nodes = []
#     settlement_variable = 0
#     angular_displacement_variable = 0
#     equilibrium_equation_variable = ""
#     node_reaction_variable = 0
#     for i in range(number_of_nodes):
#         beam_nodes.append("")
#         beam_nodes[i] = Node(settlement_variable, angular_displacement_variable, equilibrium_equation_variable,
#                              node_reaction_variable)

#     list_of_unknown_angular_displacements = []
#     first_node = "A"
#     for i in range(number_of_nodes):
#         if i != 0 and i != number_of_nodes - 1:
#             beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
#             list_of_unknown_angular_displacements.append(beam_nodes[i].angular_displacement)
#         else:
#             beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
#             beam_nodes[i].angular_displacement = 0

#         first_node = chr(ord(first_node) + 1)

#     class Span:
#         def __init__(self, left_fem, right_fem, span_length, load, loading_condition, cord_rotation, left_moment,
#                      right_moment, left_slope_deflection_equation, right_slope_deflection_equation,
#                      reaction_at_left_node_on_span, reaction_at_right_node_on_span, span_a_value):
#             self.left_fem = left_fem
#             self.right_fem = right_fem
#             self.span_length = span_length
#             self.load = load
#             self.loading_condition = loading_condition
#             self.cord_rotation = cord_rotation
#             self.left_moment = left_moment
#             self.right_moment = right_moment
#             self.left_slope_deflection_equation = left_slope_deflection_equation
#             self.right_slope_deflection_equation = right_slope_deflection_equation
#             self.reaction_at_left_node_on_span = reaction_at_left_node_on_span
#             self.reaction_at_right_node_on_span = reaction_at_right_node_on_span
#             self.span_a_value = span_a_value

#     beam_spans = []
#     left_fem_variable = 1
#     right_fem_variable = 1
#     span_length_variable = 1
#     load_variable = 1
#     loading_condition_variable = ""
#     cord_rotation_variable = 1
#     left_moment_variable = 1
#     right_moment_variable = 1
#     left_slope_deflection_equation_variable = ""
#     right_slope_deflection_equation_variable = ""
#     reaction_at_left_node_on_span_variable = 1
#     reaction_at_right_node_on_span_variable = 1
#     span_a_value_variable = 1

#     for i in range(number_of_spans):
#         beam_spans.append("")
#         beam_spans[i] = Span(left_fem_variable, right_fem_variable, span_length_variable, load_variable,
#                              loading_condition_variable, cord_rotation_variable, left_moment_variable,
#                              right_moment_variable, left_slope_deflection_equation_variable,
#                              right_slope_deflection_equation_variable, reaction_at_left_node_on_span_variable,
#                              reaction_at_right_node_on_span_variable, span_a_value_variable)

#     length_of_beam = 0
#     for i, span_data in enumerate(spans_data):
#         beam_spans[i].loading_condition = span_data['loadingCondition']
#         beam_spans[i].span_length = int(span_data['spanLength'])
#         beam_spans[i].load = span_data['load']

#         length_of_beam += beam_spans[i].span_length

#         if beam_spans[i].loading_condition == 'P_C':
#             beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length) / 8
#             beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

#         elif beam_spans[i].loading_condition == 'P_X':
#             beam_spans[i].span_a_value = span_data['span_a_value']
#             a = beam_spans[i].span_a_value
#             b = beam_spans[i].span_length - a
#             beam_spans[i].right_fem = int((beam_spans[i].load * b * a * a) / (beam_spans[i].span_length * beam_spans[i].span_length))
#             beam_spans[i].left_fem = int((beam_spans[i].load * b * b * a) / (beam_spans[i].span_length * beam_spans[i].span_length))

#         elif beam_spans[i].loading_condition == 'P_C_2':
#             beam_spans[i].right_fem = (2 * beam_spans[i].load * beam_spans[i].span_length) / 9
#             beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

#         elif beam_spans[i].loading_condition == 'P_C_3':
#             beam_spans[i].right_fem = float((15 * beam_spans[i].load * beam_spans[i].span_length)) / 48
#             beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

#         elif beam_spans[i].loading_condition == 'UDL':
#             beam_spans[i].right_fem = int((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 12
#             beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

#         elif beam_spans[i].loading_condition == 'UDL/2_R':
#             beam_spans[i].right_fem = float((11 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 192
#             beam_spans[i].left_fem = float(-1 * (float(5 * beam_spans[i].load) * float(beam_spans[i].span_length) * float(beam_spans[i].span_length))) / 192

#         elif beam_spans[i].loading_condition == 'UDL/2_L':
#             beam_spans[i].right_fem = float((5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 192
#             beam_spans[i].left_fem = -1 * (11 * beam_spans[i].load * beam_spans[i].span_length *
#                                        beam_spans[i].span_length) / 192

#         elif beam_spans[i].loading_condition == 'VDL_R':
#             beam_spans[i].right_fem = float((beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 20
#             beam_spans[i].left_fem = -1 * (float(beam_spans[i].load) * float(beam_spans[i].span_length) * float(beam_spans[i].span_length)) / 30

#         elif beam_spans[i].loading_condition == 'VDL_L':
#             beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
#             beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20

#         elif beam_spans[i].loading_condition == 'VDL_C':
#             beam_spans[i].right_fem = float((5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)) / 96
#             beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

#         elif beam_spans[i].loading_condition == "none":
#             beam_spans[i].right_fem = 0
#             beam_spans[i].left_fem = 0
#             print(f"No loading on span {i+1}")

#     coordinates = []
#     shear_forces = []
#     current_length = 0
#     sf = 0  # Initial shear force
#     for i in range(number_of_spans):
#         span_length = beam_spans[i].span_length
#         while current_length < span_length:
#             coordinates.append(current_length)
#             sf += beam_spans[i].left_fem  # Add left internal force at the beginning of the span
#             shear_forces.append(sf)
#             current_length += length_of_beam / 20
#         current_length -= span_length  # Adjust current_length for the next span

#     # Add the last shear force (taking into account the reaction at the last support)
#     sf += beam_nodes[-1].node_reaction
#     shear_forces.append(sf)

#     return coordinates, shear_forces

# Example usage:
# coordinates, shear_forces = beam_analysis(number_of_supports, number_of_internal_joints, spans_data)
