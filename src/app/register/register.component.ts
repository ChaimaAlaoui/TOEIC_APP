import { Component } from '@angular/core';
import { Router, RouterModule} from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true,imports: [FormsModule, CommonModule, RouterModule], 
})
export class RegisterComponent {
  passwordFieldType: string = 'password';
  firstName: string = '';
  lastName: string = '';
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  errorMessage: string = ''; 
  formValid: boolean = false; 
  statusMessage: string = ''; 
  messageType: string = ''; 
  formTouched: boolean = false;
  submitted: boolean = false; // Nouvelle variable pour suivre si le formulaire a été soumis

  errors: any = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  };

  constructor(private router: Router) {}  

  togglePasswordVisibility() {
    this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
  }

  navigateToLogin() {
    this.router.navigate(['/login']);  
  }

  validateFirstName() {
    // Ne mettre à jour formTouched que si l'utilisateur interagit directement avec ce champ
    // La validation globale sera gérée par validateAll() lors de la soumission
    this.errors.firstName = this.firstName.trim() ? '' : 'First name is required.';
    this.updateFormValid();
  }
  
  validateLastName() {
    this.errors.lastName = this.lastName.trim() ? '' : 'Last name is required.';
    this.updateFormValid();
  }

  validateEmail() {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    this.errors.email = this.email.trim() ? 
      (emailRegex.test(this.email) ? '' : 'Please enter a valid email address.') : 
      'Email is required.';
    this.updateFormValid();
  }

  validatePassword() {
    if (!this.password.trim()) {
      this.errors.password = 'Password is required.';
    } else {
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/; // Minimum 8 characters, 1 letter and 1 number
      this.errors.password = passwordRegex.test(this.password)
        ? ''
        : 'Password must contain at least 8 characters, one letter and one number.';
    }
    this.updateFormValid();
  }

  validateConfirmPassword() {
    if (!this.confirmPassword.trim()) {
      this.errors.confirmPassword = 'Password confirmation is required.';
    } else {
      this.errors.confirmPassword =
        this.password === this.confirmPassword
          ? ''
          : 'Passwords do not match.';
    }
    this.updateFormValid();
  }

  validateAll() {
    // Marquer le formulaire comme soumis pour afficher toutes les erreurs
    this.submitted = true;
    this.formTouched = true;
    
    this.validateFirstName();
    this.validateLastName();
    this.validateEmail();
    this.validatePassword();
    this.validateConfirmPassword();
  }

  updateFormValid() {
    this.formValid = (
      this.firstName.trim() !== '' &&
      this.lastName.trim() !== '' &&
      this.email.trim() !== '' &&
      this.password.trim() !== '' &&
      this.confirmPassword.trim() !== ''
    ) && Object.values(this.errors).every((error) => !error);
  }

  register() {
    this.validateAll();
    
    if (!this.formValid) {
      this.errorMessage = 'Please correct the errors before continuing.';
      return;
    }
    
    this.errorMessage = '';

    const user = {
      firstName: this.firstName,
      lastName: this.lastName,
      email: this.email,
      password: this.password,
    };

    fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        if (data.status === "success" && data.emailSent) {
          this.statusMessage = 'Your account has been successfully created. Please check your email to activate it.';
          this.messageType = 'success';
        } else if (data.status === "success" && !data.emailSent) {
          this.statusMessage = 'Your account has been created, but there was an error sending the email. Please contact support.';
          this.messageType = 'warning';
        } else {
          this.statusMessage = data.message || 'An error occurred while creating the account. Please try again.';
          this.messageType = 'error';
        }
      })
      .catch((error) => {
        console.error('Error during registration:', error);
        this.statusMessage = 'An error occurred. Please try again.';
        this.messageType = 'error';
      });
  }
}