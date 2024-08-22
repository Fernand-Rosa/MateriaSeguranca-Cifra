<h1>Exercícios</h1>
<p><a href="https://github.com/Fernand-Rosa/MateriaSeguranca-Cifra/tree/main/exercicio1">Exercício 1: Criar um programa para cifrar e decifrar arquivos.</p>
<ul>
<li>Criar um cabeçalho (32 bytes) para o arquivo encriptado que contenha os seguintes campos:</li>
<li>Identificador: 2 bytes</li>
<li>Versão: 1 byte. Inicialmente com o valor 1.</li>
<li>Algoritmo: 1 byte. Valor 1 para AES.</li>
<li>Modo: 1 byte. Valor 1 para CBC.</li>
<li>IV: 16 bytes.</li>
<li>Reserved: 11 bytes</li>
</ul>
<p>Exercício 2: Criar um programa para gerar e verificar a integridade de arquivos.</p>
<ul>
<li>Criar um cabeçalho (48 bytes) para o arquivo encriptado que contenha os seguintes campos:</li>
<li>Identificador: 2 bytes</li>
<li>Versão: 1 byte. Inicialmente com o valor 1.</li>
<li>Algoritmo: 1 byte. Valor 1 para AES.</li>
<li>Modo: 1 byte. Valor 1 para CBC.</li>
<li>IV: 16 bytes.</li>
<li>Fingerprint: 16 bytes. (valor que garante a integridade)</li>
<li>Reserved: 11 bytes</li>
</ul>
