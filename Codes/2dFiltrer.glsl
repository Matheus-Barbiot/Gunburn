uniform sampler2D bgl_RenderedTexture;
uniform vec2 bgl_RenderedTextureSize;

void main()
{
    // Tamanho da resolução simulada 160x120 320x240 256x224
    vec2 resolution = vec2(320, 240);

    // Coordenadas de tela
    vec2 uv = gl_TexCoord[0].st;

    // Quantiza as coordenadas para simular baixa resolução
    vec2 pixelUV = floor(uv * resolution) / resolution;

    // Pega a cor da textura renderizada na coordenada "pixelada"
    vec4 color = texture2D(bgl_RenderedTexture, pixelUV);

    // Define a cor final
    gl_FragColor = color;
}
