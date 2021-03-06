#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 24 de mar de 2019

@author: zeller
'''
#===============================================================================
#                                     Imports
#===============================================================================
## To work with images
from PIL import Image
## To make HTTP requests
import requests
## To open images as bytes
from io import BytesIO
## To display images
# from IPython.display import display
## To create matrix from images
import numpy as np
## To generate random int values
from random import randint

#===============================================================================
#                                    Constants
#===============================================================================
BANDS = 3
CLUSTER_INDEX = 3
DEFAULT_MATRIX_TYPE = 'uint8'
DEFAULT_RBG_VALUE = ( 0, 0, 0 )
DEFAULT_PIXEL_VALUE = MAX_PIXEL_VALUE = 255
MIN_PIXEL_VALUE = 0
DEFAULT_NUMBER_OF_CLUSTERS = 3
DEFAULT_TOLERANCE_VALUE_FOR_CLUSTER_CHANGE = 1
DEFAULT_THRESHOLD_VALUE = 128
DEAFULT_MAX_STEPS_THRESHOLD = 10
DEFAULT_DELTA_THRESHOLD = 2
DEFAULT_HORIZONTAL_REGIONS = 3
DEFAULT_VERTICAL_REGIONS = 3
GREY_SCALE_MAX_VALUE = 256
HISTOGRAM_HEIGHT = 256
HISTOGRAM_WIDTH = 511
MAX_PIXEL_INDEX, MIN_PIXEL_INDEX = 1, 0
MODE = 'RGB'
R, G, B = 0, 1, 2
SIZE = ( 200, 300 )
START_IMAGE_HEIGHT = 0
START_IMAGE_WIDTH = 0
PUND_LUMINOSITY_MODES = {
    "BT709": [0.2125, 0.7154, 0.0721],
    "RMY": [0.5, 0.419, 0.081],
    "Y": [0.299, 0.587, 0.114]
    }
X_KERNEL, Y_KERNEL = 0, 1


#===============================================================================
#                                 Image Manipulation
#===============================================================================
def load_image_url ( url ):
    """Carrega imagem a partir de url
    Args:
        url: url da imagem a ser carregada
    Returns:
        Um novo objeto imagem (Pillow.Image)
        
    """
    imagem_remota = requests.get( url )
    return Image.open( BytesIO( imagem_remota.content ) )


def load_image_path ( path ):
    """Carrega imagem a partir de path relativo
    Args:
        path: path da imagem a ser carregada
    Returns:
        Um novo objeto imagem (Pillow Image)
    """
    return Image.open( path )


def new_image ( image_size = SIZE, color_mode = MODE, pixel_rgb_value = DEFAULT_RBG_VALUE ):
    """Cria nova imagem (Pillow.Image)
    Args:
        color_mode: esquema de cores da imagem
        image_size: tupla contendo o width e higth da imagem. Default = ( 200, 300 )
        pixel_rbg_value: valor de cada pixel nos canais R, G e B
    Returns:
        Um novo objeto imagem (Pillow image)
    """
    return Image.new( color_mode, image_size, pixel_rgb_value )


def load_image_data ( image ):
    """Carrega dados da imagem
    Args:
        image: imagem com dados a serem carregados
    Returns:
        Um novo objeto imagem
    """
    return image.load()

def numpy_array_from_matrix(matrix, matrix_Type = DEFAULT_MATRIX_TYPE ):
    return np.asarray( matrix ).astype( matrix_Type )

def matrix_from_image( lines, columns, bands = BANDS, pixel_value = DEFAULT_PIXEL_VALUE ):
    """Cria matriz de pixels
    Args:
        lines: nÃƒÂºmero de linhas da matriz (height)
        columns: nÃƒÂºmero de colunas da matriz (width)
        bands: nÃƒÂºmero de bandas (dimensoes) da imagem. Default = 3 (BANDS)
        pixel_value: valor atribuido a cada pixel da imagem. Default = 255 (DEFAULT_PIXEL_VALUE)
    Returns:
        Matriz com n=bands dimensoes de pixels
    """
    return [ [ [ band * 0 + pixel_value for band in range( bands ) ] for column in range( columns ) ] for line in range( lines ) ]


def image_from_matrix( rgb_matrix, matrix_Type = DEFAULT_MATRIX_TYPE, color_mode = MODE ):
    """Cria imagem a partir de matriz
    Args:
        rgb_matrix: matriz tridimensional representando imagem
        canais R, G e B.
        matrix_Type: tipo de dados da matriz, default = uint8
        mode: image color scheme. Default = 'RGB'
    Returns:
        new Pillow Image
    """
    return Image.fromarray( numpy_array_from_matrix(rgb_matrix, matrix_Type), color_mode )


def find_min_image_height ( images ):
    """Retorna menor altura dentre lista de imagens
    Args:
        images: lista de imagens
    Returns:
        menor altura
    """
    return min( image.height for image in images )


def find_min_image_width( images ):
    """Retorna menor largura dentre lista de imagens
    Args:
        images: lista de imagens
    Returns:
        menor largura
    """
    return min( image.width for image in images )


def new_kernel ( lines = 3, columns = 3 ):
    """Cria kernel a partir de lines e columns (linhas e colunas)
    Args:
        lines: nÃƒÂºmero de linhas do kernel, default = 3
        columns: nÃƒÂºmero de colunas do kernel, default = 3
    Returns:
        kernel (lines x columns)
    """
    return [ [ line * 0 + 1 for line in range( lines ) ] for column in range( columns ) ]


def new_laplacian_kernel ( lines = 3, columns = 3, pound = -8 ):
    """Cria kernel laplacianao 
    Args:
        lines: nÃƒÂºmero de linhas do kernel, default = 3
        columns: nÃƒÂºmero de colunas do kernel, default = 3
        pound: peso central do kernel. Default = -8
    Returns:
        kernel (lines x columns)
    """
    laplacian_kernel = [ [ line * 0 + 1 for line in range( lines ) ] for column in range( columns ) ]
    
    laplacian_kernel[start_kernel_height( laplacian_kernel )][start_kernel_width( laplacian_kernel )] = pound
    
    return laplacian_kernel


def find_kernel_width( kernel ):
    """Descobre largura do kernel (width)
    Args:
        kernel: kernel que se deseja-se descobrir largura
    Returns:
        largura do kernel
    """
    return len( kernel[0] )


def find_kernel_height( kernel ):
    """Descobre altura do kernel (width)
    Args:
        kernel: kernel que se deseja-se descobrir altura
    Returns:
        altura do kernel
    """
    return len( kernel )


def start_kernel_width ( kernel ):
    """Descobre largura mÃƒÂ¡xima para excursÃƒÂ£o do kernel
    Args:
        kernel: kernel que se deseja-se descobrir largura
        mÃƒÂ¡xima para movimentaÃƒÂ§ÃƒÂ£o (excursÃƒÂ£o)
    Returns:
        largura mÃƒÂ¡xima para excursÃƒÂ£o
    """
    kernel_width = find_kernel_width( kernel )
    
    return kernel_width // 2


def start_kernel_height ( kernel ):
    """Descobre altura mÃƒÂ¡xima para excursÃƒÂ£o do kernel
    Args:
        kernel: kernel que se deseja-se descobrir altura
        mÃƒÂ¡xima para movimentaÃƒÂ§ÃƒÂ£o (excursÃƒÂ£o)
    Returns:
        altura mÃƒÂ¡xima para excursÃƒÂ£o
    """
    kernel_height = find_kernel_height( kernel )
    
    return kernel_height // 2


def get_image_width ( image ):
    return len( image[0] )


def get_image_height ( image ):
    return len( image )

def get_random_image_position_x(image_height):
    return randint(0, image_height)

def get_random_image_position_y(image_width):
    return randint(0, image_width)

def generate_k_means_matrix (image):
    return matrix_from_image(image.height, image.width, bands=4, pixel_value=0)

def new_image_color_cluster_list(number_of_clusters, bands=BANDS):
    return [ [ band * 0 for band in range(bands) ] for cluster in range( number_of_clusters ) ] 

def generate_random_cluster_values_from_image(image, clusters):
    base_image = load_image_data(image)
    cluster_size = len(clusters)
    
    for cluster in range(cluster_size):
        cluster_rgb_random_values = []
        random_image_position_x = get_random_image_position_x(image.height - 1)
        random_image_position_y = get_random_image_position_y(image.width - 1)
        for band in range(BANDS):
            cluster_rgb_random_values.append( base_image[random_image_position_y, random_image_position_x][band] )
        
        clusters[cluster] = cluster_rgb_random_values
    
    return clusters

def generate_k_means_rgb_cluster_from_image(image, number_of_clusters = DEFAULT_NUMBER_OF_CLUSTERS):
    clusters = new_image_color_cluster_list(number_of_clusters)
    return generate_random_cluster_values_from_image(image, clusters)
     

def generate_rbg_cluster_structure(clusters):
    return [ [ [ band * 0 for band in range( len( clusters[0] ) ) ], 0 ] for cluster in range(len(clusters)) ]

def find_pixel_cluster(image_data, image_position_x, image_position_y, clusters):
    image_rgb_values = [ 
                        image_data[image_position_y, image_position_x][R],
                        image_data[image_position_y, image_position_x][G],
                        image_data[image_position_y, image_position_x][B]
                       ]
    cluster_value_based_on_image = []
    for cluster in range(len(clusters)):
        cluster_value_based_on_image.append(
            ( 
                ( ( image_rgb_values[R] - clusters[cluster][R] )**2 ) + 
                ( ( image_rgb_values[G] - clusters[cluster][G] )**2 ) + 
                ( ( image_rgb_values[B] - clusters[cluster][B] )**2 )
                
            )**(1/2) 
        )
    
    return cluster_value_based_on_image.index(min(cluster_value_based_on_image))

def recalculate_clusters_values(cluster_data):
    new_clusters = []
    for cluster_index in range(len(cluster_data)):
        if cluster_data[cluster_index][1] > 0:
            new_clusters.append( [ 
                cluster_data[cluster_index][0][R] // cluster_data[cluster_index][1],
                cluster_data[cluster_index][0][G] // cluster_data[cluster_index][1],
                cluster_data[cluster_index][0][B] // cluster_data[cluster_index][1] 
            ] )
        else:
            new_clusters.append(cluster_data[cluster_index][0])
            
    return new_clusters

def verify_cluster_change(new_cluster_values, old_cluster_values, tolerance_value_for_cluster_change=DEFAULT_TOLERANCE_VALUE_FOR_CLUSTER_CHANGE):
    is_change = False
    
    for cluster_index in range(len(new_cluster_values)):
        for cluster_item in range(len(new_cluster_values[0] ) ):
            is_change = True if ( 
                abs( new_cluster_values[cluster_index][cluster_item] - old_cluster_values[cluster_index][cluster_item] ) 
                ) <= tolerance_value_for_cluster_change else False 
    
    return is_change

def matrix_image_from_key_means_image(k_means_matrix):
    return numpy_array_from_matrix(k_means_matrix, DEFAULT_MATRIX_TYPE)[:, :, :3]

def image_from_k_means_matrix(k_means_matrix, clusters):
    matrix_image_height = get_image_height(k_means_matrix)
    matrix_image_width = get_image_width(k_means_matrix)
    
    for cluster_index in range(len(clusters)):
        for image_position_x in range(matrix_image_height):
            for image_position_y in range(matrix_image_width):
                if ( k_means_matrix[image_position_x][image_position_y][CLUSTER_INDEX] == cluster_index ):
                    k_means_matrix[image_position_x][image_position_y][R] = clusters[cluster_index][R]
                    k_means_matrix[image_position_x][image_position_y][G] = clusters[cluster_index][G]
                    k_means_matrix[image_position_x][image_position_y][B] = clusters[cluster_index][B]
                    
    return image_from_matrix( matrix_image_from_key_means_image( k_means_matrix ) )

def generate_sobel_kernel ( ):
    """Cria kernel de Sobel
    Returns:
        Tupla de kernels [ A (horizonal) e B (vertical) ]
    """
    x_kernel = [ [ -1, 0, 1 ], [ -1, 0, 1 ], [ -1, 0, 1 ] ]
    y_kernel = [ [ 1, 1, 1 ], [ 0, 0, 0 ], [ -1, -1, -1 ] ]
    
    return [x_kernel, y_kernel]

#===============================================================================
#                                DIP Algorithms
#===============================================================================
def find_rgb_image_bounds( matrix_image_data, matrix_image_width, matrix_image_height ):
    """Econtra maior e menor valor de pixel dada uma imagem
    Args:
        image: matriz da image
        matrix_image_width: largura da matriz da imagem
        matrix_image_height: altura da matriz da imagem
    Returns: lista contendo maior e menor valor de cada canal
    """
    min_pixel_value = None
    max_pixel_value = None
    image_bounds = [[], [], []]
    
    for band in range ( BANDS ):
        for position_x in range( matrix_image_height ):
            for position_y in range( matrix_image_width ):
                if min_pixel_value == None or matrix_image_data[position_x][position_y][band] < min_pixel_value:
                    min_pixel_value = matrix_image_data[position_x][position_y][band]
                if max_pixel_value == None or matrix_image_data[position_x][position_y][band] > max_pixel_value:
                    max_pixel_value = matrix_image_data[position_x][position_y][band]
                        
        image_bounds[band] = [ min_pixel_value, max_pixel_value ]
        
    return image_bounds
            

def normalize_rgb_image ( matrix_image ):
    """Normaliza imagem utilzando regra de trÃƒÂªs simples
    Args:
        matrix_image: matriz de imagem RGB
    Returns: matriz de imagem RGB com valores dos pixels normalizados
    """    
    image_width = get_image_width( matrix_image )
    image_height = get_image_height( matrix_image )
    
    imageBound = find_rgb_image_bounds( matrix_image, image_width, image_height )
    
    fator_ajuste_r = 255 / ( imageBound[R][MAX_PIXEL_INDEX] - imageBound[R][MIN_PIXEL_INDEX] )
    fator_ajuste_g = 255 / ( imageBound[G][MAX_PIXEL_INDEX] - imageBound[G][MIN_PIXEL_INDEX] )
    fator_ajuste_b = 255 / ( imageBound[B][MAX_PIXEL_INDEX] - imageBound[B][MIN_PIXEL_INDEX] )
    
    for position_x in range( image_height ):
        for position_y in range( image_width ):
            matrix_image[position_x][position_y] = ( 
                            ( fator_ajuste_r * ( matrix_image[position_x][position_y][R] - imageBound[R][0] ) ),
                            ( fator_ajuste_g * ( matrix_image[position_x][position_y][G] - imageBound[G][0] ) ),
                            ( fator_ajuste_b * ( matrix_image[position_x][position_y][B] - imageBound[B][0] ) )
                          )
    
    return matrix_image


def add_images( images, normalize_result = False, color_mode = MODE ):
    """Soma N imagens tratando overflow com truncamento ou normalizaÃƒÂ§ÃƒÂ£o
    Args: 
        images: lista de imagens
        normalize_result: indica truncamento(False) ou normalizaÃƒÂ§ÃƒÂ£o(True), default=False
        color_mode = 'color color_mode' da imagem resultante, defaul='RGB'
    Returns:
        Um objeto de imagem contendo a soma de todas as 
        imagens.
    """
    new_image_width = find_min_image_width( images )
    new_image_height = find_min_image_height( images )
    
    base_matrix_image = matrix_from_image( new_image_height, new_image_width )
    
    for image in range( len( images ) - 1 ):
        image1 = load_image_data( images[image] )
        image2 = load_image_data( images[image + 1] )
        for position_x in range( new_image_height ):
            for position_y in range( new_image_width ):
                base_matrix_image[position_x][position_y] = ( 
                                   image1[position_y, position_x][R] + image2[position_y, position_x][R],
                                   image1[position_y, position_x][G] + image2[position_y, position_x][G],
                                   image1[position_y, position_x][B] + image2[position_y, position_x][B]
                                  )
    if( normalize_result ):
        base_matrix_image = normalize_rgb_image( base_matrix_image )
        
    return image_from_matrix( base_matrix_image )


def subtract_images( images, normalize_result = False, color_mode = MODE ):
    """Subtrai N imagens tratando overflow com truncamento ou normalizacao
    Args: 
        images: lista de imagens
        normalize_result: indica truncamento(False) ou normalizaÃƒÂ§ÃƒÂ£o(True), default=False
        color_mode = 'color color_mode' da imagem resultante, defaul='RGB'
    Returns:
        Um objeto de imagem contendo a subtraÃƒÂ§ÃƒÂ£o de todas as 
        imagens.
    """
    new_image_width = find_min_image_width( images )
    new_image_height = find_min_image_height( images )
    
    baseImage = matrix_from_image( new_image_height, new_image_width )
    
    for image in range( len( images ) - 1 ):
        image1 = load_image_data( images[image] )
        image2 = load_image_data( images[image + 1] )
        for position_x in range( new_image_height ):
            for position_y in range( new_image_width ):
                baseImage[position_x][position_y] = (
                                   image1[position_y, position_x][R] - image2[position_y, position_x][R],
                                   image1[position_y, position_x][G] - image2[position_y, position_x][G],
                                   image1[position_y, position_x][B] - image2[position_y, position_x][B]
                                  )
    if( normalize_result ):
        baseImage = normalize_rgb_image( baseImage )
        
    return image_from_matrix( baseImage )


def multiply_images( images, normalize_result = False, color_mode = MODE ):
    """Multiplica N imagens
    Args: 
        images: lista de imagens
        normalize_result: indica truncamento(False) ou normalizaÃƒÂ§ÃƒÂ£o(True), default=False
        color_mode = 'color color_mode' da imagem resultante, defaul='RGB'
    Returns:
        Um objeto de imagem contendo a multiplicaÃƒÂ§ÃƒÂ£o de todas as 
        imagens.
    """
    new_image_width = find_min_image_width( images )
    new_image_height = find_min_image_height( images )
    
    baseImage = matrix_from_image( new_image_height, new_image_width )
    
    for image in range( len( images ) - 1 ):
        image1 = load_image_data( images[image] )
        image2 = load_image_data( images[image + 1] )
        for position_x in range( new_image_height ):
            for position_y in range( new_image_width ):
                baseImage[position_x][position_y] = ( 
                                   image1[position_y, position_x][R] * image2[position_y, position_x][R],
                                   image1[position_y, position_x][G] * image2[position_y, position_x][G],
                                   image1[position_y, position_x][B] * image2[position_y, position_x][B]
                                  )
    if( normalize_result ):
        baseImage = normalize_rgb_image( baseImage )
        
    return image_from_matrix( baseImage )


def half_median_filter ( image, kernel = new_kernel( 3, 3 ) ):
    
    result_image = matrix_from_image( image.height, image.width )
    base_image = load_image_data( image )
    
    for image_position_x in range( image.height ):
        for image_position_y in range( image.width ):
            
            start_position_x = 0 if image_position_x - start_kernel_height( kernel ) <= 0 else image_position_x - start_kernel_height( kernel )
            end_position_x = image_position_x if image_position_x + start_kernel_height( kernel ) >= image.height - 1 else image_position_x + start_kernel_height( kernel )
            
            start_position_y = 0 if image_position_y - start_kernel_width( kernel ) <= 0 else image_position_y - start_kernel_width( kernel )
            end_position_y = image_position_y if image_position_y + start_kernel_width( kernel ) >= image.width - 1 else image_position_y + start_kernel_width( kernel )
            
            kernelSize = ( end_position_x + 1 - start_position_x ) * ( end_position_y + 1 - start_position_y )
            
            for band in range( BANDS ):
                for kernel_position_x in range( start_position_x, end_position_x + 1 ):
                    kernelX = ( end_position_x ) - kernel_position_x
                    for kernel_position_y in range( start_position_y, end_position_y + 1 ):
                        kernelY = ( end_position_y ) - kernel_position_y
                        result_image[image_position_x][image_position_y][band] += base_image[start_position_y + kernelY, start_position_x + kernelX][band] * kernel[kernelY][kernelX]
                        
                result_image[image_position_x][image_position_y][band] /= kernelSize
            
    result_image = normalize_rgb_image( result_image )
    return image_from_matrix( result_image )


def median_filter ( image, kernel = new_kernel( 3, 3 ) ):
    
    result_image = matrix_from_image( image.height, image.width )
    base_image = load_image_data( image )
    
    start_kernel_x = start_kernel_height( kernel )
    start_kernel_y = start_kernel_width( kernel )
    
    neighborhood_pixel_values = []
    
    for image_position_x in range( image.height ):
        
        start_position_x = 0 if image_position_x - start_kernel_x <= 0 else image_position_x - start_kernel_x
        end_position_x = image_position_x if image_position_x + start_kernel_x >= image.height - 1 else image_position_x + start_kernel_x
        
        for image_position_y in range( image.width ):
            
            start_position_y = 0 if image_position_y - start_kernel_y <= 0 else image_position_y - start_kernel_y
            end_position_y = image_position_y if image_position_y + start_kernel_y >= image.width - 1 else image_position_y + start_kernel_y
            
            for band in range( BANDS ):
                neighborhood_pixel_values = []
                for kernel_position_x in range( start_position_x, end_position_x + 1 ):
                    kernelX = ( end_position_x ) - kernel_position_x
                    for kernel_position_y in range( start_position_y, end_position_y + 1 ):
                        kernelY = ( end_position_y ) - kernel_position_y
                        neighborhood_pixel_values.append( base_image[start_position_y + kernelY, start_position_x + kernelX ][band] )
                        
                result_image[image_position_x][image_position_y][band] = np.median( neighborhood_pixel_values )
            
    return image_from_matrix( normalize_rgb_image( result_image ) )


def laplacian_filter( image, kernel = new_laplacian_kernel( 3, 3 ) ):
    result_image = matrix_from_image( image.height, image.width, pixel_value = 0 )
    base_image = load_image_data( image )
    
    start_kernel_x = start_kernel_height( kernel )
    start_kernel_y = start_kernel_width( kernel )
    
    for image_position_x in range( image.height ):
        
        start_position_x = 0 if image_position_x - start_kernel_x <= 0 else image_position_x - start_kernel_x
        end_position_x = image_position_x if image_position_x + start_kernel_x >= image.height - 1 else image_position_x + start_kernel_x
        
        for image_position_y in range( image.width ):
            
            start_position_y = 0 if image_position_y - start_kernel_y <= 0 else image_position_y - start_kernel_y
            end_position_y = image_position_y if image_position_y + start_kernel_y >= image.width - 1 else image_position_y + start_kernel_y
            
            for band in range( BANDS ):
                final_pixel_value = 0
                for kernel_position_x in range( start_position_x, end_position_x + 1 ):
                    kernelX = ( end_position_x ) - kernel_position_x
                    for kernel_position_y in range( start_position_y, end_position_y + 1 ):
                        kernelY = ( end_position_y ) - kernel_position_y
                        final_pixel_value = final_pixel_value + base_image[start_position_y + kernelY, start_position_x + kernelX][band] * kernel[kernelY][kernelX]
                
                result_image[image_position_x][image_position_y][band] = 0 if final_pixel_value <= 0 else final_pixel_value
    
    return image_from_matrix( normalize_rgb_image( result_image ) )

def sobel_filter( image, kernel = generate_sobel_kernel() ):
    base_image = load_image_data( image )
    result_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range( image.height ):
        for image_position_y in range( image.width ):
            
            start_position_x = 0 if image_position_x - start_kernel_height( kernel[X_KERNEL] ) <= 0 else image_position_x - start_kernel_height( kernel[X_KERNEL] )
            end_position_x = image_position_x if image_position_x + start_kernel_height( kernel[X_KERNEL] ) >= image.height - 1 else image_position_x + start_kernel_height( kernel[X_KERNEL] )
            
            start_position_y = 0 if image_position_y - start_kernel_width( kernel[X_KERNEL] ) <= 0 else image_position_y - start_kernel_width( kernel[X_KERNEL] )
            end_position_y = image_position_y if image_position_y + start_kernel_width( kernel[Y_KERNEL] ) >= image.width - 1 else image_position_y + start_kernel_width( kernel[Y_KERNEL] )
                
            
            for band in range( BANDS ):
                x_kernel_value = 0
                y_kernel_value = 0
                for kernel_position_x in range( start_position_x, end_position_x + 1 ):
                    kernelX = ( end_position_x ) - kernel_position_x
                    for kernel_position_y in range( start_position_y, end_position_y + 1 ):
                        kernelY = ( end_position_y ) - kernel_position_y
                        y_kernel_value += base_image[start_position_y + kernelY, start_position_x + kernelX][band] * kernel[X_KERNEL][kernelY][kernelX]
                        x_kernel_value += base_image[start_position_y + kernelY, start_position_x + kernelX][band] * kernel[Y_KERNEL][kernelY][kernelX]
                        
                result_image[image_position_x][image_position_y][band] = x_kernel_value
            
    return image_from_matrix( result_image )


def brightness_monocromatization ( image ):
    base_image = load_image_data( image )
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range( image.height ):
        for image_position_y in range ( image.width):
            chanelValues = [
                base_image[image_position_y, image_position_x][R],
                base_image[image_position_y, image_position_x][G],
                base_image[image_position_y, image_position_x][B]
            ]
            
            base_matrix_image[image_position_x][image_position_y][R] = ( max( chanelValues ) + min( chanelValues ) ) / 2
            base_matrix_image[image_position_x][image_position_y][G] = ( max( chanelValues ) + min( chanelValues ) ) / 2
            base_matrix_image[image_position_x][image_position_y][B] = ( max( chanelValues ) + min( chanelValues ) ) / 2
    
    return image_from_matrix( base_matrix_image )


def median_monocromatization( image ):
    base_image = load_image_data( image )
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range( image.height ):
        for image_position_y in range ( image.width):
            chanel_values = base_image[image_position_y, image_position_x][R] + base_image[image_position_y, image_position_x][G] + base_image[image_position_y, image_position_x][B]
                            
            base_matrix_image[image_position_x][image_position_y][R] = chanel_values / 3
            base_matrix_image[image_position_x][image_position_y][G] = chanel_values / 3
            base_matrix_image[image_position_x][image_position_y][B] = chanel_values / 3
    
    return image_from_matrix( base_matrix_image )


def luminosity_monocromatization( image, luminosity_mode = "BT709" ):
    chanel_pound = PUND_LUMINOSITY_MODES.get( luminosity_mode )
    base_image = load_image_data( image )
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range( image.height ):
        for image_position_y in range ( image.width ):
            chanel_values = [base_image[image_position_y, image_position_x][R], base_image[image_position_y, image_position_x][G], base_image[image_position_y, image_position_x][B]]
            base_matrix_image[image_position_x][image_position_y][R] = ( chanel_values[R] * chanel_pound[R] ) + ( chanel_values[G] * chanel_pound[G] ) + ( chanel_values[B] * chanel_pound[B] )
            base_matrix_image[image_position_x][image_position_y][G] = ( chanel_values[R] * chanel_pound[R] ) + ( chanel_values[G] * chanel_pound[G] ) + ( chanel_values[B] * chanel_pound[B] )
            base_matrix_image[image_position_x][image_position_y][B] = ( chanel_values[R] * chanel_pound[R] ) + ( chanel_values[G] * chanel_pound[G] ) + ( chanel_values[B] * chanel_pound[B] )
    
    return image_from_matrix( base_matrix_image )

def generate_base_grey_scale_frequency(grey_scale_value=GREY_SCALE_MAX_VALUE):
    return [i * 0 for i in range(grey_scale_value)]

def generate_histogram( image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y ):
    grey_scale_frequency = generate_absolute_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y)
    max_grey_scale_frequency = get_max_grey_scale_frequency( grey_scale_frequency )
    
    adjustment_factor = HISTOGRAM_HEIGHT / max_grey_scale_frequency 

    for index in range( len( grey_scale_frequency ) ):
        grey_scale_frequency[index] = int (adjustment_factor * grey_scale_frequency[index] ) 
               
    result_histogram = matrix_from_image( HISTOGRAM_HEIGHT, HISTOGRAM_WIDTH, pixel_value = 200 )

    for histogram_position_y in range( HISTOGRAM_WIDTH ):
        for histogram_position_x in range( HISTOGRAM_HEIGHT - grey_scale_frequency[histogram_position_y // 2] -1, HISTOGRAM_HEIGHT ):
            result_histogram[histogram_position_x][histogram_position_y][R] = 0
            result_histogram[histogram_position_x][histogram_position_y][G] = 0
            result_histogram[histogram_position_x][histogram_position_y][B] = 0
            
    return image_from_matrix( result_histogram )

def generate_sobel_histogram ( image ):
    base_image = load_image_data(image)
    histogram_values = [i * 0 for i in range(image.height)]
         
    for image_position_x in range( image.height ):
        for image_position_y in range ( image.width):
            if base_image[image_position_y, image_position_x][R] > 1:
                histogram_values[image_position_x] += 1            
              
    return histogram_values
    
def generate_absolute_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y):
    return generate_grey_scale_frequence(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y)

def generate_relative_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y):
    grey_scale_frequency = generate_absolute_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y)
    image_resolution = ( end_image_position_x - start_image_position_x )  * ( end_image_position_y - start_image_position_y )
    
    relative_histogram = generate_base_grey_scale_frequency()
    
    for grey_scale_index in range(len(grey_scale_frequency)):
        relative_histogram[grey_scale_index] = grey_scale_frequency[grey_scale_index] / image_resolution
        
    return relative_histogram

def generate_grey_scale_frequence(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y):
    grey_scale_frequency = generate_base_grey_scale_frequency()
    base_image = load_image_data(image)
    
    for image_position_x in range( start_image_position_x, end_image_position_x ):
        for image_position_y in range( start_image_position_y, end_image_position_y ):
            pixel_value = base_image[image_position_y, image_position_x][R]
            grey_scale_frequency[pixel_value] += 1
    
    return grey_scale_frequency
    
def get_max_grey_scale_frequency(grey_scale_frequence):
    return max( grey_scale_frequence )

def find_threshold_value(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y, max_steps_threshold=DEAFULT_MAX_STEPS_THRESHOLD, delta_threshold=DEFAULT_DELTA_THRESHOLD):
    relative_histogram = generate_relative_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y)
    threshold_value = DEFAULT_THRESHOLD_VALUE
    print(f'Find Threshold Values - Steps: {max_steps_threshold}, Delta: {delta_threshold} ')
    
    while max_steps_threshold > 0:
        max_steps_threshold -= 1
        left_half_median_brightness = 0
        right_half_median_brightness = 0
        
        for index in range(1, len(relative_histogram)):
            if index < threshold_value:
                left_half_median_brightness += index * relative_histogram[index]
            else:
                right_half_median_brightness += index * relative_histogram[index]
        
        new_threshold_value = ( left_half_median_brightness + right_half_median_brightness ) // 2
        print(f'Calculated Threshold Value: {new_threshold_value}')
        
        if abs(new_threshold_value - threshold_value) < delta_threshold:
            break
        
        threshold_value = new_threshold_value
    return threshold_value
        

def find_threshold_value_based_on_histogram_weight(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y, max_steps_threshold=DEAFULT_MAX_STEPS_THRESHOLD, delta_threshold=DEFAULT_DELTA_THRESHOLD):
    relative_histogram = generate_relative_histogram(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y)
    threshold_value = DEFAULT_THRESHOLD_VALUE
    left_landmark = MIN_PIXEL_VALUE
    right_landmark = MAX_PIXEL_VALUE
    
    print(f'Find Threshold Values Based on Histogram Weight - Steps: {max_steps_threshold}, Delta: {delta_threshold} \n')
    
    while max_steps_threshold > 0:
        max_steps_threshold -= 1
        left_histogram_weight = 0
        right_histogram_weight = 0
        
        for index in range(1, len(relative_histogram)):
            if index < threshold_value:
                left_histogram_weight += relative_histogram[index]
            else:
                right_histogram_weight += relative_histogram[index]
        
        if left_histogram_weight > right_histogram_weight:
            print(f'Left Histogram Weight: {left_histogram_weight} > Right Histogram Weight: {right_histogram_weight}\n')
            print(f'Right Landmark: {right_landmark}, Left Landmark: {left_landmark}\n')
            right_landmark = threshold_value
            threshold_value = ( left_landmark + threshold_value ) // 2
        else:
            print(f'Left Histogram Weight: {left_histogram_weight} < Right Histogram Weight: {right_histogram_weight}\n')
            print(f'Right Landmark: {right_landmark}, Left Landmark: {left_landmark}\n')
            left_landmark = threshold_value
            threshold_value = ( right_landmark + threshold_value ) // 2
            
        print(f'Calculated Threshold Value: {threshold_value}\n')
        
    return threshold_value

def threshold_image(image, start_image_position_x, start_image_position_y, end_image_position_x, end_image_position_y, threshold_value):
    base_image = load_image_data(image)
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range( start_image_position_x, end_image_position_x ):
        for image_position_y in range( start_image_position_y, end_image_position_y ):
            if base_image[image_position_y, image_position_x][R] < threshold_value:
                base_matrix_image[image_position_x][image_position_y][R] = MIN_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][G] = MIN_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][B] = MIN_PIXEL_VALUE
            else:
                base_matrix_image[image_position_x][image_position_y][R] = MAX_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][G] = MAX_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][B] = MAX_PIXEL_VALUE
                
    return image_from_matrix(base_matrix_image)

def threshold_matrix_image(image, base_matrix_image, start_matrix_position_x, start_matrix_position_y, end_matrix_position_x, end_matrix_position_y, threshold_value):
    base_image = load_image_data(image)
    
    for image_position_x in range( start_matrix_position_x, end_matrix_position_x ):
        for image_position_y in range( start_matrix_position_y, end_matrix_position_y ):
            if base_image[image_position_y, image_position_x][R] < threshold_value:
                base_matrix_image[image_position_x][image_position_y][R] = MIN_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][G] = MIN_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][B] = MIN_PIXEL_VALUE
            else:
                base_matrix_image[image_position_x][image_position_y][R] = MAX_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][G] = MAX_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][B] = MAX_PIXEL_VALUE
                
    return base_matrix_image

def global_threshold_image(image, threshod_value=None):
    threshold_value = find_threshold_value_based_on_histogram_weight(image, START_IMAGE_HEIGHT, START_IMAGE_WIDTH, image.height, image.width) if threshod_value is None else threshod_value
    print(f'Final Threshold Value: {threshold_value}')
    return threshold_image(image, START_IMAGE_HEIGHT, START_IMAGE_WIDTH, image.height, image.width, threshold_value)

def local_threshold_image(image, horizontal_regions=DEFAULT_HORIZONTAL_REGIONS, vertical_regions=DEFAULT_VERTICAL_REGIONS):
    region_width = image.width // horizontal_regions
    region_height = image.height // vertical_regions
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for horizontal_region in range(horizontal_regions):
        for vertical_region in range(vertical_regions):
            start_region_position_x = horizontal_region * region_height
            start_region_position_y = vertical_region * region_width
            end_region_position_x = start_region_position_x + region_height- 1
            end_region_position_y = start_region_position_y + region_width - 1
            
            threshold_value = find_threshold_value_based_on_histogram_weight(image, start_region_position_x, start_region_position_y, end_region_position_x, end_region_position_y)
            base_matrix_image = threshold_matrix_image(image, base_matrix_image, start_region_position_x, start_region_position_y, end_region_position_x, end_region_position_y, threshold_value)
    
    return image_from_matrix(base_matrix_image)
    

def cluster_by_k_means_method(image, number_of_clusters=DEFAULT_NUMBER_OF_CLUSTERS ):
    base_image = load_image_data(image)
    clusters = generate_k_means_rgb_cluster_from_image(image, number_of_clusters)
    old_clusters_values = []
    is_converged = False
    k_means_matrix = generate_k_means_matrix(image) 
    cluster_data = generate_rbg_cluster_structure(clusters)
    
    while is_converged == False:
        for image_position_x in range(image.height):
            for image_position_y in range(image.width):
                cluster_index = find_pixel_cluster(base_image, image_position_x, image_position_y, clusters)
                k_means_matrix[image_position_x][image_position_y][CLUSTER_INDEX] = cluster_index
                cluster_data[cluster_index][1] += 1
                cluster_data[cluster_index][0][R] += base_image[image_position_y, image_position_x][R]
                cluster_data[cluster_index][0][G] += base_image[image_position_y, image_position_x][G]
                cluster_data[cluster_index][0][B] += base_image[image_position_y, image_position_x][B]
            
        old_clusters_values = clusters
        clusters = recalculate_clusters_values(cluster_data)
        is_converged = verify_cluster_change(clusters, old_clusters_values)
        cluster_data = generate_rbg_cluster_structure(clusters)
        
    return image_from_k_means_matrix(k_means_matrix, clusters)

def find_license_plate_areas (histogram_values):
    max_value = max(histogram_values)
    candidate_value = max_value * 0.3
    second_candidate_value = candidate_value * 0.7
    license_plate_areas = [False for i in histogram_values]
    
    for index in range(len(histogram_values)):
        if histogram_values[index] > candidate_value:
            for second_index in range(index, len(histogram_values)):
                if histogram_values[second_index] > second_candidate_value and count_areas(histogram_values, second_index, second_candidate_value):    
                    license_plate_areas[second_index] = True
    
    return license_plate_areas

def show_license_plate_areas (image, license_plate_areas):
    base_image = load_image_data(image)
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range(image.height):
        for image_position_y in range(image.width):
            if license_plate_areas[image_position_x]:
                base_matrix_image[image_position_x][image_position_y][R] = base_image[image_position_y, image_position_x][R]
                base_matrix_image[image_position_x][image_position_y][G] = base_image[image_position_y, image_position_x][G]
                base_matrix_image[image_position_x][image_position_y][B] = base_image[image_position_y, image_position_x][B]
            else:
                base_matrix_image[image_position_x][image_position_y][R] = MAX_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][G] = MIN_PIXEL_VALUE
                base_matrix_image[image_position_x][image_position_y][B] = MIN_PIXEL_VALUE
    
    return image_from_matrix(base_matrix_image)

def find_license_plate (license_plate_areas, license_plate_values):
    pixels = [0,0,0,1000] # start_X, start_Y, max_value, min_value
    final = [0, 0, 0]
    flag = True
    while flag:
        flag = False
        for index in range(len(license_plate_areas)):
            if license_plate_areas[index]:
                area = []
                pixels[0] = index # start position
                for second in range(index, len(license_plate_areas)):
                    if license_plate_areas[second] == False:
                        pixels[1] = second - 1 # end position
                        break
                    area.append(license_plate_values[second])
                        
                max_value_in_area = max(area)
                min_value_in_area = min(area)
                diference = max_value_in_area - min_value_in_area
                
#                 if max_value_in_area > pixels[2]:
#                     pixels[2] = max_value_in_area
#                 if min_value_in_area < pixels[3]:
#                     pixels[3] = min_value_in_area
                    
                if diference > final[2]:
                    final = [pixels[0], pixels[1], diference]
                    flag = True
    return final


def count_areas (histogram, start, value):
    count = 0
    for index in range(start, len(histogram)):
        if histogram[index] > value:
            count += 1
            
    return count >= 20

def find_license_plates (image, start_position, end_position):
    base_image = load_image_data(image)
    base_matrix_image = matrix_from_image( image.height, image.width )
    
    for image_position_x in range(start_position, end_position):
        for image_position_y in range(image.width):
            base_matrix_image[image_position_x][image_position_y][R] = base_image[image_position_y, image_position_x][R]
            base_matrix_image[image_position_x][image_position_y][G] = base_image[image_position_y, image_position_x][G]
            base_matrix_image[image_position_x][image_position_y][B] = base_image[image_position_y, image_position_x][B]
    
    return image_from_matrix(base_matrix_image)

def create_sobel_histogram(sobel_histogram_values):
    base_matrix_image = matrix_from_image( len(sobel_histogram_values), 150, pixel_value = 200 )
    
    for image_position_x in range(get_image_height(base_matrix_image)):
        for image_position_y in range(sobel_histogram_values[image_position_x]):            
            base_matrix_image[image_position_x][image_position_y][R] = MIN_PIXEL_VALUE
            base_matrix_image[image_position_x][image_position_y][G] = MIN_PIXEL_VALUE
            base_matrix_image[image_position_x][image_position_y][B] = MIN_PIXEL_VALUE
    
    return image_from_matrix(base_matrix_image)


# image2 = load_image_path('/home/zeller/Pictures/Imagens-Teste/imagem-diferenca2.jpg')



