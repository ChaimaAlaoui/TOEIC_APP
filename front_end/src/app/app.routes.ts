import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ActivateAccountComponent } from './activate-account/activate-account.component';
import { TestComponent } from './test/test.component';

// Définir les routes de l'application
export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' } ,
  { path: 'activate-account/:token', component: ActivateAccountComponent },
  { path: 'test', component: TestComponent },
];
