# Installation

## 1. Install NodeJS

Next.JS requires a version of Node 18.17 or later.

## 2. Install dependencies
Navigate to the `kunstgraph/frontend` folder and run
```bash
npm install
```

also, make sure to generate the frontend client! To do so, run (while the backend is running, see next section)

```bash
turbo generate:client
```
or alternatively run

```bash
npm run generate:client
```

# View the Platform
To view the platform while developing, navigate to the `kunstgraph\backend` folder and run

```bash
npm run dev
```
Afterwards, do the same in the `kunstgraph\frontend` folder in a separate terminal. The terminal output should say at which address the platform can be accessed, typically it's http://localhost:3000.

# Frontend Code Structure

Most editing will happen in the `src` directory.

### src
This directory contains four subdirectories:
- `components` function as building blocks ([see README](src/components/README.md))
- `lib` contains various utility functions, hooks, and configuration settings ([see README](src/lib/README.md))
- `pages` define the structure of all pages on the platform ([see README](src/pages/README.md))
- `styles` loads Tailwind utilities inside the project

### public
This directory contains additional images that are used on the platform (e.g. the logo of JDCRP and background images for the landing page).

### Further Files
There is a collection of further files in the frontend directory. We highlight some of them here.

`.prettierrc.json` helps auto-formatting the code.

`next.config.js` defines urls on the web that we allow programs to call.

`tailwind.config.ts` contains custom settings, like, e.g., custom colors.
