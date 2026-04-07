/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		paths: {
			base: process.argv.includes('dev') ? '' : (process.env.BASE_PATH ?? '')
		}
	}
};

export default config;
