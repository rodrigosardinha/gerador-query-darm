# 📦 Guia de Distribuição - Processador de DARMs

Este guia explica como empacotar e distribuir o Processador de DARMs de diferentes formas.

## 🎯 Opções de Distribuição

### 1. 📦 Pacote Python (Recomendado)
### 2. 🚀 Executável Standalone
### 3. 🐳 Container Docker
### 4. 📁 Arquivo ZIP Simples

---

## 📦 1. Pacote Python (PyPI)

### Pré-requisitos
```bash
pip install setuptools wheel twine
```

### Construir o Pacote
```bash
# Construir distribuição
python setup.py sdist bdist_wheel

# Verificar arquivos criados
ls dist/
```

### Publicar no PyPI
```bash
# Teste primeiro no TestPyPI
twine upload --repository testpypi dist/*

# Publicar no PyPI oficial
twine upload dist/*
```

### Instalar via pip
```bash
pip install gerador-query-darm
darm-processor  # Comando disponível globalmente
```

---

## 🚀 2. Executável Standalone

### Pré-requisitos
```bash
pip install pyinstaller
```

### Criar Executável
```bash
# Executável único
pyinstaller --onefile --name darm-processor darm_processor.py

# Executável com interface gráfica (futuro)
pyinstaller --onefile --windowed --name darm-processor-gui darm_processor.py
```

### Distribuir
- Arquivo gerado em `dist/darm-processor.exe` (Windows)
- Arquivo gerado em `dist/darm-processor` (Linux/macOS)

---

## 🐳 3. Container Docker

### Construir Imagem
```bash
docker build -t darm-processor .
```

### Executar Container
```bash
# Execução simples
docker run -v $(pwd)/darms:/app/darms -v $(pwd)/inserts:/app/inserts darm-processor

# Com docker-compose
docker-compose up
```

### Distribuir Imagem
```bash
# Tag para registro
docker tag darm-processor seu-registro/darm-processor:1.0.0

# Push para registro
docker push seu-registro/darm-processor:1.0.0
```

---

## 📁 4. Arquivo ZIP Simples

### Usar Script de Distribuição
```bash
python distribute.py
```

### Conteúdo do ZIP
```
gerador-query-darm-1.0.0/
├── darm_processor.py
├── config.py
├── requirements.txt
├── README.md
├── exemplo_uso.py
├── test_darm_processor.py
├── VERSION_INFO.txt
├── install.bat (Windows)
├── install.sh (Linux/macOS)
├── darms/
└── inserts/
```

---

## 🔧 Scripts Automatizados

### Build Script
```bash
python build.py
```

Opções disponíveis:
1. Construir pacote Python
2. Instalar localmente
3. Criar executável
4. Criar Dockerfile
5. Executar tudo

### Distribuição Completa
```bash
python distribute.py
```

Cria automaticamente:
- ✅ Arquivo ZIP com estrutura completa
- ✅ Scripts de instalação para Windows/Linux
- ✅ Executável (se PyInstaller disponível)
- ✅ Informações da versão

---

## 📋 Checklist de Distribuição

### Antes da Distribuição
- [ ] Testes passando: `python test_darm_processor.py`
- [ ] Documentação atualizada
- [ ] Version number atualizada
- [ ] Dependências verificadas
- [ ] Licença incluída

### Para Pacote Python
- [ ] `setup.py` configurado
- [ ] `pyproject.toml` configurado
- [ ] `MANIFEST.in` incluído
- [ ] Metadata completa
- [ ] Entry points definidos

### Para Executável
- [ ] PyInstaller instalado
- [ ] Dependências incluídas
- [ ] Arquivos de configuração embutidos
- [ ] Teste em sistema limpo

### Para Docker
- [ ] Dockerfile otimizado
- [ ] docker-compose.yml configurado
- [ ] Volumes mapeados
- [ ] Imagem testada

---

## 🚀 Comandos Rápidos

### Desenvolvimento
```bash
# Instalar em modo desenvolvimento
pip install -e .

# Executar testes
python test_darm_processor.py

# Executar exemplo
python exemplo_uso.py
```

### Build Completo
```bash
# Opção 1: Script interativo
python build.py

# Opção 2: Distribuição completa
python distribute.py

# Opção 3: Comandos manuais
python setup.py sdist bdist_wheel
pyinstaller --onefile darm_processor.py
docker build -t darm-processor .
```

### Distribuição
```bash
# PyPI
twine upload dist/*

# Docker Hub
docker push seu-usuario/darm-processor:1.0.0

# GitHub Releases
# (fazer upload manual do ZIP)
```

---

## 📊 Comparação das Opções

| Método | Facilidade | Tamanho | Dependências | Portabilidade |
|--------|------------|---------|--------------|---------------|
| **Pacote Python** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Executável** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Docker** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **ZIP Simples** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 Recomendações

### Para Usuários Técnicos
- **Pacote Python**: Melhor para desenvolvedores e ambientes controlados
- **Docker**: Ideal para ambientes de produção e CI/CD

### Para Usuários Finais
- **Executável**: Mais fácil para usuários não técnicos
- **ZIP Simples**: Bom para distribuição interna

### Para Distribuição Pública
- **PyPI**: Para comunidade Python
- **GitHub Releases**: Para distribuição geral

---

## 🔍 Solução de Problemas

### Erro de Build
```bash
# Limpar cache
rm -rf build/ dist/ *.egg-info/
python setup.py clean --all

# Reinstalar dependências
pip install --upgrade setuptools wheel
```

### Erro de PyInstaller
```bash
# Verificar dependências
pip install pyinstaller
pyinstaller --debug darm_processor.py
```

### Erro de Docker
```bash
# Reconstruir sem cache
docker build --no-cache -t darm-processor .

# Verificar logs
docker logs darm-processor
```

---

## 📞 Suporte

Para dúvidas sobre distribuição:
- 📧 Email: rodrigo.sardinha@example.com
- 🐛 Issues: https://github.com/rodrigosardinha/gerador-query-darm/issues
- 📚 Documentação: README.md 