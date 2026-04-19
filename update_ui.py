import re
import sys

file_path = "index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def update_class(m):
    cls_str = m.group(1)
    classes = cls_str.split()
    new_classes = set(classes)
    
    # Body background
    if "bg-gradient-to-br" in new_classes and "from-slate-50" in new_classes:
        new_classes.update(['dark:from-gray-950', 'dark:via-gray-900', 'dark:to-gray-950', 'dark:text-gray-100', 'transition-colors', 'duration-500'])
        
    # Text colors
    if "text-gray-900" in new_classes: new_classes.add("dark:text-gray-100")
    if "text-gray-800" in new_classes: new_classes.add("dark:text-gray-200")
    if "text-gray-700" in new_classes: new_classes.add("dark:text-gray-300")
    if "text-gray-600" in new_classes: new_classes.add("dark:text-gray-400")
    if "text-gray-500" in new_classes: new_classes.add("dark:text-gray-400")
    if "text-gray-400" in new_classes: new_classes.add("dark:text-gray-500")
    
    # Backgrounds and borders
    if "bg-white" in new_classes:
        if "rounded-2xl" in new_classes:
            new_classes.update(["dark:bg-gray-800/80", "dark:backdrop-blur-sm", "dark:border-gray-700/50", "hover:shadow-xl", "transform", "hover:-translate-y-1", "duration-300"])
        elif "rounded-xl" in new_classes and "bg-red-50" not in new_classes:
            new_classes.update(["dark:bg-gray-800/90", "dark:border-gray-700/60", "hover:-translate-y-1", "transform", "group"])
            if "hover:border-red-300" in new_classes:
                new_classes.add("dark:hover:border-red-500")

    if "bg-gray-50" in new_classes: new_classes.update(["dark:bg-gray-900/50"])
    if "bg-red-50" in new_classes: new_classes.update(["dark:bg-gray-800/90", "transform", "transition-all", "duration-300", "hover:scale-[1.02]"])
    if "border-gray-200" in new_classes: new_classes.add("dark:border-gray-700")
    if "border-gray-300" in new_classes: new_classes.add("dark:border-gray-700")
    if "border-red-600" in new_classes: new_classes.add("dark:border-red-500")
    
    # Play buttons styling
    if "bg-red-600" in new_classes and "w-10" in new_classes:
        new_classes.discard("bg-red-600")
        new_classes.discard("hover:bg-red-700")
        new_classes.update(["bg-gradient-to-br", "from-red-500", "to-red-600", "hover:from-red-600", "hover:to-red-700", "dark:from-red-600", "dark:to-red-800", "shadow-red-500/30", "dark:shadow-red-900/50", "group-hover:rotate-12", "group-hover:scale-110", "duration-300"])
    
    # Interactions
    if "hover:bg-red-50/30" in new_classes: new_classes.add("dark:hover:bg-gray-700/50")
    if "active:bg-red-100/20" in new_classes: new_classes.add("dark:active:bg-gray-600/50")
    if "hover:shadow-lg" in new_classes: new_classes.update(["group-hover:scale-105", "active:scale-95", "duration-200"])
    
    return 'class="' + ' '.join(new_classes) + '"'

content = re.sub(r'class="([^"]*)"', update_class, content)

# Header element update for toggle button
header_match = re.search(r'<header[^>]*>', content)
if header_match:
    if 'id="theme-toggle-icon"' not in content:
        toggle_html = """
            <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width=\\'20\\' height=\\'20\\' viewBox=\\'0 0 20 20\\' xmlns=\\'http://www.w3.org/2000/svg\\'%3E%3Cg fill=\\'%23ffffff\\' fill-opacity=\\'0.05\\' fill-rule=\\'evenodd\\'%3E%3Ccircle cx=\\'3\\' cy=\\'3\\' r=\\'3\\'/%3E%3Ccircle cx=\\'13\\' cy=\\'13\\' r=\\'3\\'/%3E%3C/g%3E%3C/svg%3E')] opacity-50"></div>
            <button onclick="toggleTheme()" class="absolute top-4 right-4 bg-white/20 hover:bg-white/30 backdrop-blur-md rounded-full w-10 h-10 flex items-center justify-center transition-all shadow-sm hover:scale-110 active:scale-95 z-10" aria-label="Toggle Dark Mode">
                <span id="theme-toggle-icon" class="text-xl filter drop-shadow-md">🌙</span>
            </button>"""
        
        header_tag = content[header_match.start():header_match.end()]
        if 'relative' not in header_tag:
            new_header_tag = header_tag.replace('class="', 'class="relative overflow-hidden ')
            content = content[:header_match.start()] + new_header_tag + toggle_html + content[header_match.end():]

# Add logic config
if "darkMode: 'class'" not in content:
    script_to_add = """    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    animation: {
                        'spin-slow': 'spin 3s linear infinite',
                        'bounce-slow': 'bounce 2s infinite',
                    }
                }
            }
        }
        function toggleTheme() {
            const html = document.documentElement;
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                localStorage.theme = 'light';
                document.getElementById('theme-toggle-icon').innerText = '🌙';
            } else {
                html.classList.add('dark');
                localStorage.theme = 'dark';
                document.getElementById('theme-toggle-icon').innerText = '☀️';
            }
        }
        // Initial setup
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            document.addEventListener('DOMContentLoaded', () => {
                let el = document.getElementById('theme-toggle-icon');
                if(el) el.innerText = '☀️';
            });
        }
    </script>
"""
    content = content.replace('</head>', script_to_add + '</head>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("UI upgraded successfully.")
