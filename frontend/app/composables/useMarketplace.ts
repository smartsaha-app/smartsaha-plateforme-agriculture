import { ref } from 'vue';

export const useMarketplace = () => {
  const products = ref([]);
  const categories = ref([]);
  const cart = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const { apiFetch } = useApi();

  const fetchProducts = async (params = {}) => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/marketplace/products/', { params });
      products.value = response.results || response; // Handle pagination if present
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await apiFetch('/api/marketplace/categories/');
      categories.value = response.results || response;
    } catch (err: any) {
      console.error('Error fetching categories:', err);
    }
  };

  const fetchCart = async () => {
    try {
      const response = await apiFetch('/api/marketplace/cart/');
      // Cart ViewSet returns a list by default or the single cart if get_object is used
      cart.value = Array.isArray(response) ? response[0] : response;
    } catch (err: any) {
      console.error('Error fetching cart:', err);
    }
  };

  const addToCart = async (productId: number, quantity: number = 1) => {
    try {
      const response = await apiFetch('/api/marketplace/cart/add_item/', {
        method: 'POST',
        body: {
          product_id: productId,
          quantity: quantity
        }
      });
      cart.value = response;
      return response;
    } catch (err: any) {
      throw err;
    }
  };

  const removeFromCart = async (itemId: number) => {
    try {
      const response = await apiFetch('/api/marketplace/cart/remove_item/', {
        method: 'POST',
        body: {
          item_id: itemId
        }
      });
      cart.value = response;
      return response;
    } catch (err: any) {
      throw err;
    }
  };

  const checkout = async (deliveryData: any) => {
    try {
      const response = await apiFetch('/api/marketplace/cart/checkout/', {
        method: 'POST',
        body: deliveryData
      });
      cart.value = null; 
      return response;
    } catch (err: any) {
      throw err;
    }
  };

  return {
    products,
    categories,
    cart,
    loading,
    error,
    fetchProducts,
    fetchCategories,
    fetchCart,
    addToCart,
    removeFromCart,
    checkout
  };
};
