# ERPNext Custom App - AppMart

This repository contains a custom app called AppMart for ERPNext, which extends the functionality of the ERPNext system. AppMart provides a marketplace-like feature where users can browse and install additional apps and modules to enhance their ERPNext experience.

## Installation

To install this custom app in your ERPNext instance, follow these steps:

1. Clone the repository using the following command:
   ```
   git clone https://github.com/ShahzadNaser/appmart.git
   ```

2. Change your working directory to the appmart folder:
   ```
   cd appmart
   ```

3. Create a new branch (optional):
   ```
   git checkout -b <branch_name>
   ```

4. Install the app in your ERPNext instance:
   ```
   bench --site <site_name> install-app appmart
   ```

5. Start the ERPNext development server:
   ```
   bench start
   ```

6. Access your ERPNext instance in a web browser:
   ```
   http://localhost:8000
   ```

## Features

- Browse and search for additional apps and modules.
- Install and manage installed apps.
- Provides a user-friendly interface for app management.

## Contributing

We welcome contributions to enhance the functionality of AppMart. If you would like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your development environment.
3. Create a new branch for your feature or bug fix:
   ```
   git checkout -b <branch_name>
   ```
4. Make the necessary changes and commit them.
5. Push your changes to your forked repository.
6. Submit a pull request from your forked repository to the main repository.

Please ensure that your code adheres to the coding standards and includes appropriate documentation.

## License

This ERPNext custom app is licensed under the [MIT License](LICENSE). Feel free to modify and distribute it as per the terms of the license.

## Contact

If you have any questions or need assistance, you can reach out to the maintainer of this project:

- Name: Shahzad Naser
- GitHub: [ShahzadNaser](https://github.com/ShahzadNaser)

Please provide clear and detailed information when reporting any issues.

## Acknowledgments

We would like to express our gratitude to the ERPNext community and contributors for their continuous support and feedback.
