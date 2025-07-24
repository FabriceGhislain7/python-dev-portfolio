# 🌟 Portfolio Fabrice Ghislain

> Portfolio personale moderno e responsive - Python Developer & AI/ML Enthusiast

[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://fabriceghislain7.github.io/portfolio/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/FabriceGhislain7/portfolio)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📖 Panoramica

Portfolio personale sviluppato con **HTML5**, **CSS3** e **JavaScript vanilla** per mostrare le mie competenze, progetti e percorso professionale come sviluppatore Python e specialista in AI/ML.

### ✨ Caratteristiche Principali

- 🎨 **Design Moderno**: Interface pulita e professionale
- 📱 **Completamente Responsive**: Ottimizzato per tutti i dispositivi
- 🌓 **Tema Scuro/Chiaro**: Switch dinamico tra temi
- ⚡ **Performance Ottimizzate**: Caricamento veloce e smooth
- 🎯 **SEO Friendly**: Meta tags e struttura ottimizzata
- ♿ **Accessibile**: Conforme alle linee guida WCAG
- 🎭 **Animazioni Fluide**: Transizioni e effetti CSS/JS
- 📊 **Dati Dinamici**: Caricamento progetti e skills da JSON

## 🚀 Demo Live

👉 **[Visualizza Portfolio](https://fabriceghislain7.github.io/portfolio/)**

## 🛠️ Tecnologie Utilizzate

### Frontend
- **HTML5** - Markup semantico
- **CSS3** - Styling moderno con Grid/Flexbox
- **JavaScript ES6+** - Interattività e dinamismo
- **JSON** - Storage dati progetti e competenze

### Tools & Workflow
- **Git** - Version control
- **GitHub Pages** - Hosting
- **VS Code** - Development environment
- **Chrome DevTools** - Debugging e testing

### Librerie & Risorse
- **Font Awesome** - Iconografia
- **Google Fonts** - Typography (Inter, Fira Code)
- **Intersection Observer API** - Animazioni scroll

## 📁 Struttura Progetto

```
portfolio/
├── 📁 assets/
│   ├── 📁 css/
│   │   ├── variables.css      # CSS custom properties
│   │   ├── base.css          # Stili base e reset
│   │   ├── components/       # Componenti modulari
│   │   ├── responsive.css    # Media queries
│   │   └── ...
│   ├── 📁 js/
│   │   ├── config.js         # Configurazione globale
│   │   ├── modules/          # Moduli JavaScript
│   │   └── main.js          # Script principale
│   ├── 📁 data/
│   │   ├── skills.json       # Dati competenze
│   │   └── projects.json     # Dati progetti
│   └── 📁 images/           # Asset immagini
├── 📄 index.html            # Pagina principale
├── 📄 manifest.json         # PWA manifest
├── 📄 robots.txt           # SEO robots
├── 📄 sitemap.xml          # SEO sitemap
└── 📄 README.md            # Documentazione
```

## 🎯 Sezioni Portfolio

### 🏠 Hero Section
- Presentazione personale
- Links social e contatti
- Call-to-action principali

### 👨‍💻 About
- Bio e background
- Statistiche e achievements
- Competenze trasversali
- Lingue e certificazioni

### 🛠️ Skills
- Competenze tecniche organizzate per categoria
- Livelli di expertise visualizzati
- Tecnologie e strumenti utilizzati
- Filtri dinamici per categoria

### 💼 Projects
- Portfolio progetti con dettagli completi
- Filtri per categoria e tecnologia
- Modal con screenshot e informazioni
- Links GitHub e demo live

### 🎓 Education
- Percorso formativo e titoli
- Timeline interattiva
- Corsi e certificazioni

### 📞 Contact
- Form di contatto funzionale
- Informazioni di contatto
- Links social media
- Mappa/localizzazione

## 🚀 Installazione e Utilizzo

### Prerequisiti
- Browser moderno (Chrome, Firefox, Safari, Edge)
- Server web locale (opzionale per development)

### Clone Repository
```bash
git clone https://github.com/FabriceGhislain7/portfolio.git
cd portfolio
```

### Avvio Locale
```bash
# Opzione 1: Apertura diretta
open index.html

# Opzione 2: Server Python (se installato)
python -m http.server 8000

# Opzione 3: Server Node.js (se installato)
npx http-server
```

### Deploy su GitHub Pages
1. Fork del repository
2. Vai su Settings → Pages
3. Seleziona source: Deploy from branch
4. Branch: main, Folder: / (root)
5. Save e attendi il deploy

## ⚙️ Personalizzazione

### Modifica Dati Personali
1. **Informazioni base**: Modifica `assets/js/config.js`
2. **Progetti**: Aggiorna `assets/data/projects.json`
3. **Competenze**: Modifica `assets/data/skills.json`
4. **Immagini**: Sostituisci in `assets/images/`

### Customizzazione Stili
1. **Colori**: Modifica `assets/css/variables.css`
2. **Typography**: Aggiorna font in `assets/css/typography.css`
3. **Layout**: Personalizza `assets/css/components/`

### Funzionalità Extra
- **Analytics**: Aggiungi Google Analytics in `index.html`
- **Form Backend**: Integra servizio per form contatti
- **CMS**: Connetti headless CMS per gestione contenuti

## 📊 Performance

### Lighthouse Scores
- 🎯 **Performance**: 95+
- ♿ **Accessibility**: 100
- 🔍 **SEO**: 100
- ⚡ **Best Practices**: 95+

### Ottimizzazioni Implementate
- ✅ Immagini ottimizzate e lazy loading
- ✅ CSS e JS minificati
- ✅ Critical CSS inline
- ✅ Resource hints (preload, prefetch)
- ✅ Service Worker per caching
- ✅ Compressione Gzip

## 🔧 Tecnical Features

### Architettura CSS
- **CSS Custom Properties** per theming
- **Mobile-first** responsive design
- **Modulare** con componenti riutilizzabili
- **BEM metodology** per naming conventions

### JavaScript Features
- **ES6+ syntax** con modules
- **Async/await** per API calls
- **Intersection Observer** per animations
- **Debouncing** per performance
- **Error handling** robusto

### Accessibility
- **Semantic HTML** structure
- **ARIA labels** e roles
- **Keyboard navigation** support
- **Screen reader** compatibility
- **High contrast** mode support

## 🤝 Contributing

I contributi sono benvenuti! Per contribuire:

1. Fork il progetto
2. Crea feature branch (`git checkout -b feature/nuova-feature`)
3. Commit modifiche (`git commit -m 'Aggiunge nuova feature'`)
4. Push branch (`git push origin feature/nuova-feature`)
5. Apri Pull Request

### Linee Guida
- Segui le convenzioni di codice esistenti
- Aggiungi commenti per codice complesso
- Testa su multiple browser/dispositivi
- Aggiorna documentazione se necessario

## 📝 Changelog

### v1.0.0 (2025-01-24)
- 🎉 Rilascio iniziale
- ✨ Design responsive completo
- 🌓 Sistema tema scuro/chiaro
- 📊 Caricamento dinamico dati
- 🎯 Ottimizzazioni SEO e performance
- ♿ Compliance accessibilità

## 📄 License

Questo progetto è sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per dettagli.

## 👨‍💻 Autore

**Fabrice Ghislain**
- 🌐 Portfolio: [fabriceghislain7.github.io/portfolio](https://fabriceghislain7.github.io/portfolio/)
- 📧 Email: [tua-email@esempio.com]
- 💼 LinkedIn: [linkedin.com/in/fabrice-ghislain]
- 🐙 GitHub: [@FabriceGhislain7](https://github.com/FabriceGhislain7)

## 🙏 Ringraziamenti

- Font Awesome per le icone
- Google Fonts per i font
- GitHub Pages per l'hosting gratuito
- Community open source per ispirazione

---

⭐ **Se questo progetto ti è utile, lascia una stella!** ⭐