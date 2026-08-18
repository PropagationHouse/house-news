import io

p = 'index.html'
s = io.open(p, encoding='utf-8').read()

# The corrupted form line - match by its distinctive parts
old = '''<form onsubmit="event.preventDefault();this.querySelector('button').textContent='Subscribed'''
idx = s.find(old)
if idx == -1:
    print("NOT FOUND - form line")
else:
    # find the end of the form tag
    end = s.find('>', idx)
    replacement = '''<form action="subscribe.html" method="get" onsubmit="var e=this.querySelector('input[type=email]');if(e&&e.value){e.name='email';}">'''
    s = s[:idx] + replacement + s[end+1:]
    # also ensure the input has name="email"
    s = s.replace('<input type="email" placeholder="your@email.com" required>',
                  '<input type="email" name="email" placeholder="your@email.com" required>')
    io.open(p, 'w', encoding='utf-8').write(s)
    print("REPLACED form in", p)
