# Financial Empowerment Card Generator Prompt

This document describes the prompt that generates the Financial Empowerment Card Generator script.

## Prompt Description

Create a Python script that generates PDF files containing financial empowerment cards with the following features and requirements:

1. Input:
   - A text file containing financial empowerment messages, one per line
   - Command-line arguments for specifying page sizes and custom output names

2. Output:
   - PDF files with a grid of cards, each containing a financial empowerment message
   - Support for multiple page sizes (letter, legal, A4, A3, A2, A1, A0, ledger)
   - Customizable grid layout (default 3x3)

3. Card Design:
   - Each card should have a background image
   - Text should be centered both horizontally and vertically within each card
   - Cards should have a border with a customizable color

4. Fonts and Text:
   - Use a custom TTF font (Anton-Regular) for text rendering
   - Support for Unicode characters in the text

5. Customization:
   - Configurable cell padding and spacing
   - Customizable font and border colors
   - Ability to specify a custom prefix for output filenames

6. Code Structure:
   - Implement the solution using SOLID principles
   - Use appropriate design patterns to separate concerns
   - Include detailed comments explaining the purpose and functionality of each component

7. Documentation:
   - Create a README.md file with installation instructions, usage examples, and configuration options
   - Include examples of how to run the script with different options and expected results

8. Error Handling:
   - Provide informative error messages for invalid input or configuration

9. Performance:
   - Efficiently handle the generation of multiple PDFs in a single run

10. Extensibility:
    - Design the code to be easily extendable for future enhancements, such as additional page sizes or layout options

The resulting script should be a robust, well-documented, and flexible tool for generating financial empowerment cards in various formats and sizes.