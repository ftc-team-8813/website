# Build system documentation

### Introduction
This site uses a custom build system (in imitation of
[Jekyll](https://jekyllrb.com), except it only uses Python 3).
The build script and source files are in this directory, and
the generated HTML is put into the top level directory so that
GitHub Pages can serve it.

### Building the site
First, make sure you have Python 3 installed:   
`python --version`  
Then you can simply run  
`python builder.py`  

### Syntax
Builder commands are contained in HTML comments, like so:  
```html
<!-- $command [parameter] -->
```  
Each command must be in its own line; the line containing the
command will be removed from the output.  
Files start with a header, which is terminated by a `$begin`
command. In the header, you can set the template to use and
the output directory:
```html
<!-- Set the template to use; if not set, the builder will copy the
file directly -->
<!-- $template home.html -->  

<!-- Set the output directory, relative to the location of the build
script (don't use this on templates!) -->
<!-- $output ../spam -->

<!-- Start the page; WILL THROW AN ERROR IF NOT INCLUDED -->
<!-- $begin -->
```

### Pages and Templates
The build script generates webpages by using **page** files and
**template** files.  
Pages usually include templates and set the content
to substitute in for each *section* in the template:  

```html
<!-- A sample page file -->
<!-- $template template.html -->
<!-- $begin -->

<!-- Define a section 'main', which can be included by the template -->
<!-- $section main -->
<h2> Hello World! </h2>
<p> This is some sample content </p>
<!-- Use $endsection to end the section -->
<!-- $endsection -->
```

If a page does not
use a template file, it will be copied directly to the output. If it does,
however, all content **must** be inside a section, otherwise it will be
removed:
```html
<p> This content will be removed because it's in the header </p>
<!-- $begin -->
<p> This content is not in  section, so it will be removed </p>
<!-- $section main -->
<p> This content is in the 'main' section </p>
<!-- $endsection -->
```

Templates are differentiated from normal pages by their placement
in the `templates` directory. As mentioned previously, templates can
include sections from pages:
```html
<!-- This is a sample template -->
<!-- Although they don't usually have anything in the header,
the $begin IS required -->

<!-- $begin -->
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="stylesheet.css">
    <!-- Include a section named 'head' for custom header data here -->
    <!-- $include head -->
  </head>
  <body>
    <!-- Include the main section here -->
    <!-- $include main -->
  </body>
</html>
```

Templates and pages can also include the content of other files using the
`$include-file` command.

You can also create sub-templates:

```html
<!-- This is a sub-template of the above one -->
<!-- The content goes inside the sections defined above; undefined
sections can still be used by the page or template that uses this
template -->

<!-- Include the template -->
<!-- $template template.html -->
<!-- $begin -->
<!-- $section main -->
<header>
  <p> This is our HTML5 header </p>
</header>
<main>
  <!-- We can move the main section here -->
  <!-- $include main -->
</main>
<footer>
  <p> This is our HTML5 footer </p>
</footer>
<!-- $endsection -->
```

### Using Markdown for Pages

Many of you who use GitHub might be wondering if you can use Markdown
to generate your page content. Although this isn't technically supported,
you can install a Markdown generator and use that to generate your
pages. Since Markdown supports HTML syntax, you can even put the page
file metadata into your Markdown file, like so:

```markdown
<!-- $template template.html -->
<!-- $begin -->
<!-- $section main -->
# Markdown
1. Easy to use
2. Fast to generate
3. Awesome!
<!-- $endsection -->
```
