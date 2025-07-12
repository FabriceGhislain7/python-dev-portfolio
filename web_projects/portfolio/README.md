# 🚀 Portfolio Dinamico - Sviluppatore Web

Un portfolio moderno, dinamico e completamente responsive realizzato con HTML5, CSS3 e JavaScript vanilla. Caratterizzato da animazioni fluide, tema scuro/chiaro e design all'avanguardia.

![Portfolio Preview](assets/images/portfolio-preview.png)

## ✨ Caratteristiche Principali

### 🎨 **Design & UX**
- **Design Moderno**: Interfaccia pulita con elementi glassmorphism
- **Tema Scuro/Chiaro**: Switch automatico con preferenze utente
- **100% Responsive**: Ottimizzato per desktop, tablet e mobile
- **Animazioni Fluide**: Transizioni ed effetti sofisticati
- **Micro-interazioni**: Feedback visivo su ogni azione

### ⚡ **Performance & Tecnologie**
- **Vanilla JavaScript**: Nessuna dipendenza esterna
- **CSS Grid & Flexbox**: Layout moderni e flessibili
- **Lazy Loading**: Caricamento ottimizzato delle immagini
- **PWA Ready**: Supporto Progressive Web App
- **SEO Optimized**: Meta tags e struttura semantica

### 🛠️ **Funzionalità Avanzate**
- **Navigazione Intelligente**: Smooth scroll e menu mobile
- **Filtri Progetti**: Sistema di filtri dinamici con animazioni
- **Form Contatti**: Validazione in tempo reale e auto-save
- **Sistema Particelle**: Effetti parallax e particelle interattive
- **Gestione Stato**: LocalStorage per preferenze utente

## 📁 Struttura del Progetto

```
portfolio/
├── 📄 index.html                 # Homepage principale
├── 📄 404.html                   # Pagina errore personalizzata
├── 📁 assets/
│   ├── 📁 css/
│   │   ├── 🎨 reset.css         # Reset CSS moderno
│   │   ├── 🎨 variables.css     # Variabili CSS personalizzabili
│   │   ├── 🎨 main.css          # Stili principali
│   │   ├── 🎨 components.css    # Componenti specifici
│   │   ├── 🎨 animations.css    # Animazioni e transizioni
│   │   ├── 🎨 responsive.css    # Design responsive
│   │   └── 🎨 dark-theme.css    # Tema scuro
│   ├── 📁 js/
│   │   ├── ⚙️ config.js         # Configurazioni centrali
│   │   ├── 🔧 utils.js          # Funzioni utility
│   │   ├── 🚀 main.js           # Logica principale
│   │   ├── 📁 modules/
│   │   │   ├── 🌙 theme.js      # Gestione temi
│   │   │   ├── 🧭 navigation.js # Navigazione
│   │   │   ├── 🎬 animations.js # Sistema animazioni
│   │   │   ├── 📜 scroll.js     # Gestione scroll
│   │   │   ├── 🔍 filters.js    # Filtri progetti
│   │   │   └── 📧 contact.js    # Form contatti
│   │   ├── 🧭 navigation.js     # Navigazione aggiuntiva
│   │   └── 📋 projects.js       # Gestione progetti
│   ├── 📁 images/
│   │   ├── 📁 hero/             # Immagini sezione hero
│   │   ├── 📁 projects/         # Screenshot progetti
│   │   └── 📁 icons/            # Icone personalizzate
│   ├── 📁 fonts/                # Font personalizzati
│   └── 📁 videos/               # Video di background
├── 📁 components/
│   ├── 📄 header.html           # Header componente
│   ├── 📄 footer.html           # Footer componente
│   ├── 📄 hero.html             # Sezione hero
│   ├── 📄 about.html            # Sezione about
│   ├── 📄 skills.html           # Sezione competenze
│   ├── 📄 projects.html         # Sezione progetti
│   └── 📄 contact.html          # Sezione contatti
├── 📁 data/
│   ├── 📊 skills.json           # Dati competenze
│   ├── 📊 projects.json         # Dati progetti
│   ├── 📊 experience.json       # Esperienza lavorativa
│   └── 📊 testimonials.json     # Testimonianze
├── 📁 docs/
│   ├── 📖 setup.md              # Guida installazione
│   └── 📖 deployment.md         # Guida deployment
├── 📄 manifest.json             # PWA manifest
├── 📄 robots.txt                # SEO robots
├── 📄 sitemap.xml               # Sitemap
└── 📄 README.md                 # Documentazione
```

## 🚀 Installazione e Setup

### 1. **Clone Repository**
```bash
git clone https://github.com/tuousername/portfolio.git
cd portfolio
```

### 2. **Esegui Script Struttura** (opzionale)
```bash
python3 structure.py
```

### 3. **Personalizza Contenuti**

#### **📊 Modifica Dati JSON**
```json
// data/skills.json
{
  "skills": [
    {
      "name": "JavaScript",
      "level": 90,
      "category": "Frontend"
    }
  ]
}
```

#### **🎨 Personalizza Colori**
```css
/* assets/css/variables.css */
:root {
  --primary-color: #2563eb;
  --accent-color: #06b6d4;
  --bg-color: #ffffff;
}
```

#### **⚙️ Configura API**
```javascript
// assets/js/config.js
const CONFIG = {
  contact: {
    endpoint: 'https://your-api-endpoint.com/contact'
  }
};
```

### 4. **Sostituisci Immagini**
- `assets/images/hero/profile.jpg` - Foto profilo
- `assets/images/projects/` - Screenshot progetti
- `favicon.ico` - Favicon personalizzato

## 🎨 Personalizzazione

### **Colori e Temi**
Modifica il file `assets/css/variables.css` per personalizzare:
- Colori primari e secondari
- Sfondi e bordi
- Ombre e gradienti
- Font e spaziature

### **Animazioni**
Personalizza `assets/css/animations.css` per:
- Velocità transizioni
- Effetti hover
- Animazioni scroll
- Keyframes personalizzati

### **Contenuti**
Aggiorna i file JSON in `data/` per:
- Competenze e tecnologie
- Portfolio progetti
- Esperienza lavorativa
- Informazioni personali

## 📱 Responsive Design

### **Breakpoints**
- **Mobile**: < 768px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px - 1279px
- **Large Desktop**: > 1280px

### **Ottimizzazioni Mobile**
- Menu hamburger animato
- Touch gestures
- Ottimizzazione performance
- Immagini responsive

## 🔧 Configurazioni Avanzate

### **Form Contatti**
```javascript
// Configura endpoint in config.js
CONFIG.contact.endpoint = 'https://formspree.io/f/your-id';
```

### **Analytics**
```html
<!-- Aggiungi in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
```

### **PWA Setup**
```json
// manifest.json
{
  "name": "Il Tuo Portfolio",
  "short_name": "Portfolio",
  "start_url": "/",
  "display": "standalone"
}
```

## 🌐 Deployment

### **GitHub Pages**
1. Push su repository GitHub
2. Vai su Settings > Pages
3. Seleziona source branch (main)
4. Il sito sarà disponibile su `username.github.io/portfolio`

### **Netlify**
1. Collega repository GitHub
2. Build command: nessuno (sito statico)
3. Publish directory: `/` (root)
4. Deploy automatico ad ogni push

### **Vercel**
1. Importa progetto da GitHub
2. Framework preset: Other
3. Deploy con un click

## 🎯 Features in Dettaglio

### **🎬 Sistema Animazioni**
- Scroll-triggered animations
- Stagger animations
- Particle system
- Parallax effects
- Magnetic buttons
- 3D tilt effects

### **🔍 Filtri Progetti**
- Filtri per categoria
- Ricerca testuale
- Ordinamento dinamico
- Animazioni transizioni
- URL state management

### **📧 Form Contatti**
- Validazione real-time
- Auto-save localStorage
- Character counting
- Floating labels
- Error handling
- Success notifications

### **🌙 Gestione Temi**
- Light/Dark mode
- System preference detection
- Smooth transitions
- LocalStorage persistence
- CSS custom properties

## 🚀 Performance

### **Ottimizzazioni**
- ✅ Lazy loading immagini
- ✅ Intersection Observer
- ✅ Debounced scroll events
- ✅ CSS animations GPU-accelerated
- ✅ Minified assets
- ✅ Reduced motion support

### **Lighthouse Scores**
- 🟢 Performance: 95+
- 🟢 Accessibility: 100
- 🟢 Best Practices: 100
- 🟢 SEO: 100

## 🔒 Sicurezza

- ✅ HTTPS only
- ✅ Content Security Policy
- ✅ XSS protection
- ✅ Form validation
- ✅ Rate limiting
- ✅ GDPR compliant

## 🤝 Contribuire

1. Fork del progetto
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Ringraziamenti

- [Font Awesome](https://fontawesome.com/) per le icone
- [Google Fonts](https://fonts.google.com/) per i font
- [Unsplash](https://unsplash.com/) per le immagini placeholder

## 📞 Supporto

Se hai domande o problemi:

- 📧 Email: your.email@example.com
- 💬 GitHub Issues: [Apri un issue](https://github.com/tuousername/portfolio/issues)
- 🐦 Twitter: [@tuousername](https://twitter.com/tuousername)

---

**Realizzato con ❤️ da [Il Tuo Nome](https://github.com/tuousername)**

*Ultimo aggiornamento: Gennaio 2025*