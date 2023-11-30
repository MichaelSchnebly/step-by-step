import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.arrays import vbo
import glfw
import glm
import imgui


# class LineRenderer:
#     '''Renders lines in 2D or 3D -- single shader used for all lines
#     '''
#     def __init__(self, lines):
#         self.lines = lines

#         self.vao = glGenVertexArrays(1)
#         glBindVertexArray(self.vao)

#         vertex_shader = load_shader("shaders/2D/line/vertex.glsl", GL_VERTEX_SHADER)
#         geometry_shader = load_shader("shaders/2D/line/geometry.glsl", GL_GEOMETRY_SHADER)
#         fragment_shader = load_shader("shaders/2D/line/fragment.glsl", GL_FRAGMENT_SHADER)
#         self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

#         glUseProgram(self.shader)

#         self.transform_loc = glGetUniformLocation(self.shader, "transform")
#         self.width_loc = glGetUniformLocation(self.shader, "lineWidth")
#         self.color_loc = glGetUniformLocation(self.shader, "lineColor")

#         glUseProgram(0)
#         glBindVertexArray(0)

#     def render(self):
#         for line in self.lines:
#             glUseProgram(self.shader)
#             glBindVertexArray(self.vao)

#             line.vbo.bind()
#             glEnableVertexAttribArray(0)
#             glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

#             glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, line.transform)
#             glUniform1f(self.width_loc, line.width)
#             glUniform4fv(self.color_loc, 1, line.color)

#             glDrawArrays(GL_LINE_STRIP, 0, line.vertices.shape[0])

#             line.vbo.unbind()


class IMURenderer:
    '''Renders polylines in 2D or 3D -- single shader used for all polylines
    '''
    def __init__(self, lines):
        self.lines = lines

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertex_shader = load_shader("shaders/2D/polyline/vertex.glsl", GL_VERTEX_SHADER)
        geometry_shader = load_shader("shaders/2D/polyline/geometry.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = load_shader("shaders/2D/polyline/fragment.glsl", GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

        glUseProgram(self.shader)

        self.transform_loc = glGetUniformLocation(self.shader, "transform")
        self.width_loc = glGetUniformLocation(self.shader, "lineWidth")
        self.color_loc = glGetUniformLocation(self.shader, "lineColor")

        glUseProgram(0)
        glBindVertexArray(0)

    def render(self):
        for line in self.lines:
            glUseProgram(self.shader)
            glBindVertexArray(self.vao)

            line.vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

            glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, line.transform)
            glUniform1f(self.width_loc, line.width)
            glUniform4fv(self.color_loc, 1, line.color)

            glDrawArrays(GL_LINE_STRIP_ADJACENCY, 0, line.vertices.shape[0])

            line.vbo.unbind()

def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as file:
        shader_src = file.read()
    shader_ref = glCreateShader(shader_type)
    glShaderSource(shader_ref, shader_src)
    glCompileShader(shader_ref)

    # Check for shader compilation errors
    compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
    if not compile_success:
        info_log = glGetShaderInfoLog(shader_ref)
        print(f"Shader compilation error: {info_log}")
        return None

    return shader_ref