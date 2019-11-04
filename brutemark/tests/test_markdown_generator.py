from brutemark.markdown import markdown

test_input =\
"""# Hello World
This is a test to see how the assembler/renderer logic actually works.  
This should be split with a br tag.

    This is a code block
    that spans 
    multiple lines
    
1. First item
  * nested unordered list
  * Second element
2. Second Line
"""

expected_output =\
"""<h1>Hello World</h1>
<p>This is a test to see how the assembler/renderer logic actually works.  <br/>
This should be split with a br tag.</p>


<pre><code>This is a code block
that spans 
multiple lines</code></pre>


<ol>
    <li><p>First item</p>
    <ul>
        <li>nested unordered list</li>
        <li>Second element</li>
    </ul></li>
    <li>Second Line</li>
</ol>
"""

def test_full_run_test_of_markdown_function():
    actual_output = markdown(test_input)

    assert actual_output == expected_output