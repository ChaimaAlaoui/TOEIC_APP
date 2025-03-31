import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [FormsModule, CommonModule, RouterLink]
})
export class LoginComponent {
  passwordFieldType: string = 'password';

  email: string = '';
  password: string = '';
  errorMessage: string = '';
  statusMessage: string = '';
  messageType: string = '';

  errors: any = {
    email: '',
    password: '',
  };

  constructor(private router: Router) {}

  togglePasswordVisibility() {
    this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
  }

  validateEmail() {
    if (!this.email) {
      this.errors.email = 'Email is required';
      return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    this.errors.email = emailRegex.test(this.email)
      ? ''
      : 'Please enter a valid email address';
  }

  validatePassword() {
    if (!this.password) {
      this.errors.password = 'Password is required';
      return;
    }
    
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
    this.errors.password = passwordRegex.test(this.password)
      ? ''
      : 'Password must be at least 8 characters with at least one letter and one number';
  }

  hasErrors(): boolean {
    return Object.values(this.errors).some(error => error !== '');
  }

  login() {
    // Validate all fields on submit
    this.validateEmail();
    this.validatePassword();
    
    // Check if there are any validation errors
    if (this.hasErrors()) {
      this.errorMessage = 'Please correct the errors before continuing';
      return;
    }

    const userCredentials = {
      email: this.email,
      password: this.password,
    };

    fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userCredentials),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.status === 'success' && data.accountActivated) {
          this.statusMessage = 'Login successful. Welcome!';
          this.messageType = 'success';
          this.router.navigate(['/home']);  
        } else if (data.status === 'success' && !data.accountActivated) {
          this.statusMessage = 'Your account is not activated yet. Please check your email.';
          this.messageType = 'error';
        } else {
          this.statusMessage = 'Incorrect username or password.';
          this.messageType = 'error';
        }
      })
      .catch((error) => {
        console.error('Error during login:', error);
        this.statusMessage = 'An error occurred. Please try again.';
        this.messageType = 'error';
      });
  }
}