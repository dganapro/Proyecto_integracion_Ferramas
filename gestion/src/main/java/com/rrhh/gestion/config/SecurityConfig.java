package com.rrhh.gestion.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .authorizeHttpRequests(authz -> authz
                // Permitir acceso público a endpoints de autenticación
                .requestMatchers("/api/auth/**").permitAll()
                // Permitir acceso a H2 console para desarrollo
                .requestMatchers("/h2-console/**").permitAll()
                // Permitir acceso a endpoints públicos
                .requestMatchers("/api/auth/registro", "/api/auth/login").permitAll()
                .requestMatchers("/api/auth/roles", "/api/auth/verificar-usuario/**").permitAll()
                // Endpoints específicos para administradores
                .requestMatchers("/api/admin/**").permitAll() // Por ahora permitimos acceso libre
                // Endpoints específicos para usuarios
                .requestMatchers("/api/usuario/**").permitAll() // Por ahora permitimos acceso libre
                // Endpoints generales de usuarios
                .requestMatchers("/api/usuarios/**").permitAll() // Por ahora permitimos acceso libre
                // Todos los demás endpoints existentes
                .requestMatchers("/api/**").permitAll()
                // Cualquier otra petición requiere autenticación
                .anyRequest().authenticated()            )
            .headers(headers -> headers
                .frameOptions(frameOptions -> frameOptions.disable()) // Para H2 console
            )
            .sessionManagement(session -> session.sessionCreationPolicy(
                org.springframework.security.config.http.SessionCreationPolicy.STATELESS
            ));

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(Arrays.asList("*"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}