#include "gumbo.h"
int main() {
  GumboOutput* output = gumbo_parse("<h1>Hello, World!</h1>");
  // Do stuff with output->root
  gumbo_destroy_output(&kGumboDefaultOptions, output);
}