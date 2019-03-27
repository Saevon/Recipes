# Positioning

The following become positioning elements


# Stacking Context
[](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Positioning/Understanding_z_index/The_stacking_context)

Root (html)
Transforms
Position (abs, rel, fixed, sticky)
Opacity


# Display
[](https://www.smashingmagazine.com/2018/05/guide-css-layout/)

## Flex Box:
    [](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)






## Floating

### Create a parent group that auto-clears any floats (to ensure they take up vertical (block) space)

```css
.float-group::after {
  content: "";
  display: table;
  clear: both;
}
```

